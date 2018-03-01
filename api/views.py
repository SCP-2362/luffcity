from django.db.models import F
from django.http import JsonResponse

from rest_framework.views import APIView


from api.utils import my_serializers as my_seri

from . import models


class LoginView(APIView):
    """登录API"""

    def post(self, request, *args, **kwargs):
        res = {
            "state": 10000,
            "data": None,
            "msg": None,
        }
        try:
            # 获取用户名和密码并验证
            username = request.data.get("username", '')
            password = request.data.get("password", '')
            user = models.Account.objects.filter(username=username, password=password).first()

            if user:
                # 更新token
                user_auth = models.UserAuthToken.objects.filter(user=user)
                if user_auth:
                    user_auth.update(user=user)
                else:
                    models.UserAuthToken.objects.create(user=user)

                res["data"] = {
                    "username": username,
                    "token": user.userauthtoken.token
                }
            else:
                res["state"] = 40000,
                res["msg"] = "用户名或密码错误"
        except Exception as e:
            res["state"] = 40000
            res["msg"] = "出错啦！"
        return JsonResponse(res)

    def options(self, request, *args, **kwargs):
        request.query_params
        return JsonResponse({
            "state": 10000,
            "data": None,
            "msg": None
        })


class CoursesView(APIView):
    """课程列表API"""

    def get(self, request, *args, **kwargs):
        res = {
            "state": 10000,
            "data": None,
            "msg": None
        }
        wrong_res = {
            "state": 40000,
            "data": None,
            "msg": None
        }
        try:
            # 课程详细
            if kwargs.get("pk"):
                course_obj = models.Course.objects.filter(pk=kwargs.get("pk")).first()
                if not course_obj:
                    wrong_res["msg"] = "不存在的ID"
                    return JsonResponse(wrong_res)

                # 根据筛选类型返回数据
                if request.query_params.get("data_type") == "detail":
                    detail_obj = models.CourseDetail.objects.filter(course=course_obj).first()

                    if detail_obj:
                        ser = my_seri.CourseDetailSerializer(instance=detail_obj)
                    else:
                        wrong_res["msg"] = "暂无课程详细"
                        return JsonResponse(wrong_res)
                elif request.query_params.get("data_type") == "chapters":
                    chapter_list = course_obj.coursechapters.all()
                    ser = my_seri.CourseChapterSerializer(instance=chapter_list, many=True)
                elif request.query_params.get("data_type") == "question":
                    # 根据课程去找问题
                    # questiion_list = course_obj.oftenaskedquestion_set.all()
                    from django.contrib.contenttypes.models import ContentType
                    print(course_obj._meta.model_name, '表名')
                    ct_id = ContentType.objects.filter(app_label='api', model=course_obj._meta.model_name).first().id
                    o_list = models.OftenAskedQuestion.objects.filter(content_type_id=ct_id, object_id=course_obj.id)
                    print(o_list)
                    ser = my_seri.CourseQuestionSerializer(instance=o_list, many=True)
                else:
                    ser = my_seri.CourseSerializer(instance=course_obj)
            else:
                # 课程列表
                course_list = models.Course.objects.all()
                ser = my_seri.CourseSerializer(instance=course_list, many=True)
            res["data"] = ser.data
        except Exception as e:
            print(e)
            res["state"] = 40000
            res["msg"] = "出错啦！"
        return JsonResponse(res)

    def options(self, request, *args, **kwargs):
        return JsonResponse({
            "state": 10000,
            "data": None,
            "msg": None
        })


class DegreeView(APIView):
    def get(self, request, *args, **kwargs):
        res = {
            "state": 10000,
            "data": None,
            "msg": None
        }
        try:
            if kwargs.get("pk"):
                degree_obj = models.DegreeCourse.objects.filter(pk=kwargs.get("pk")).first()
                if request.query_params.get("data_type") == "detail":
                    pass
                else:
                    ser = my_seri.DegreeCourseSerializer(degree_obj)
            else:
                degree_list = models.DegreeCourse.objects.all()
                ser = my_seri.DegreeCourseSerializer(instance=degree_list, many=True)
            res["data"] = ser.data
        except Exception as e:
            res["state"] = 40000
            res["msg"] = "出错啦！"
        return JsonResponse(res)

    def options(self, request, *args, **kwargs):
        return JsonResponse({
            "state": 10000,
            "data": None,
            "msg": None
        })


class NewsView(APIView):
    def get(self, request, *args, **kwargs):
        result = {
            "state": 10000,     # 默认为10000
            "data": '',
            "msg": None
        }
        try:
            pk = kwargs.get('pk')
            if pk:
                art_obj = models.Article.objects.get(id=pk)
                ret = my_seri.ArticleContentSerializer(instance=art_obj)
            else:
                article = models.Article.objects.all()
                ret = my_seri.ArticleSerializer(instance=article, many=True)
            result['data'] = ret.data
            return JsonResponse(result)
        except Exception as e:
            result['state'] = 40000
            result['msg'] = str(e)
            return JsonResponse(result)

    def post(self, request, *args, pk=None, **kwargs):
        result = {
            "state": '',
            "data": '',
            "msg": None
        }
        try:
            pk = pk
            userToken = request.data.get('userToken')
            UserAuthToken = models.UserAuthToken.objects.filter(token=userToken).first()
            TypeID = models.ContentType.objects.filter(app_label='api', model='article').first()
            print(TypeID, '对象')
            agree_obj = models.Agree.objects.filter(object_id=UserAuthToken.user_id, account_id=pk)
            if not agree_obj:
                models.Agree.objects.create(content_type=TypeID, object_id=UserAuthToken.user_id, account_id=pk)
                models.Article.objects.filter(id=pk).update(agree_num=F('agree_num') + 1)
                art_obj = models.Article.objects.get(id=pk)
                ret = my_seri.ArticleContentSerializer(instance=art_obj)
                result['state'] = 10000
                result['data'] = ret.data
            else:
                result['state'] = 40000
                result['msg'] ='已经点过赞，不需要重新点赞'
            return JsonResponse(result)
        except Exception as e:
            result['state'] = 40000
            result['msg'] = str(e)
            return JsonResponse(result)


class NewsViewSC(APIView):
    def post(self, request, *args, **kwargs):
        result = {
            "state": 10000,
            "data": '',
            "msg": None
        }
        try:
            pk = kwargs.get('pk')
            userToken=request.data.get('userToken')
            UserAuthToken = models.UserAuthToken.objects.filter(token=userToken).first()
            TypeID = models.ContentType.objects.filter(app_label='api', model='article').first()
            print(TypeID,'对象')
            agree_obj = models.Collection.objects.filter(object_id=UserAuthToken.user_id, account_id=pk)
            if not agree_obj:
                models.Collection.objects.create(content_type=TypeID, object_id=UserAuthToken.user_id, account_id=pk)
                models.Article.objects.filter(id=pk).update(collect_num=F('collect_num') + 1)
                art_obj = models.Article.objects.get(id=pk)
                ret = my_seri.ArticleContentSerializer(instance=art_obj)
                result['state'] = 10000
                result['data'] = ret.data
            else:
                result['state'] = 40000
                result['msg'] ='已经收藏，不要重新收藏'
            return JsonResponse(result)
        except Exception as e:
            result['state'] = 40000
            result['msg'] = str(e)
            return JsonResponse(result)

