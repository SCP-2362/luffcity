import datetime
from rest_framework.response import Response
from django.http import JsonResponse
from rest_framework.views import APIView
from rest_framework import serializers
from api.utils import my_serializers as my_seri

from . import models
class LoginView(APIView):
    def post(self, request, *args, **kwargs):
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

            res = JsonResponse({
                "state": 10000,
                "data": {
                    "username": username,
                    "token": user.userauthtoken.token
                },
                "msg": None
            })
        else:
            res = JsonResponse({
                "state": 40000,
                "data": None,
                "msg": "用户名或密码错误"
            })
        return res

    def options(self, request, *args, **kwargs):
        return JsonResponse({
            "state": 10000,
            "data": None,
            "msg": None
        })

# class CourseSerializer(serializers.ModelSerializer):
#     class Meta:
#         model = models.Course
#         fields = '__all__'
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
        if kwargs.get("pk"):
            course_obj = models.Course.objects.filter(pk=kwargs.get("pk")).first()
            if not course_obj:
                wrong_res["msg"] = "不存在的ID"
                return JsonResponse(wrong_res)
            print(request.query_params)
            if request.query_params.get("data_type") == "detail":
                detail_obj = models.CourseDetail.objects.filter(course=course_obj).first()
                if detail_obj:
                    ser = my_seri.CourseDetailSerializer(instance=detail_obj)
                else:
                    wrong_res["msg"] = "暂无课程详细"
                    return JsonResponse(wrong_res)
            elif request.query_params.get("data_type") == "chapter":
                ser = my_seri.CourseChapterSerializer(instance=course_obj)
            elif request.query_params.get("data_type") == "question":
                #根据课程去找问题
                # questiion_list = course_obj.oftenaskedquestion_set.all()
                from django.contrib.contenttypes.models import ContentType
                print(course_obj._meta.model_name,'表名')
                ct_id = ContentType.objects.filter(app_label='api', model=course_obj._meta.model_name).first().id
                o_list = models.OftenAskedQuestion.objects.filter(content_type_id=ct_id, object_id=course_obj.id)
                ser = my_seri.CourseQuestionSerializer(instance=o_list, many=True)
            else:
                ser = my_seri.CourseSerializer(instance=course_obj)
        else:
            course_list = models.Course.objects.all()
            ser = my_seri.CourseSerializer(instance=course_list, many=True)
        print(ser.data)
        res["data"] = ser.data
        return JsonResponse(res)

    def options(self, request, *args, **kwargs):
        return JsonResponse({
            "state": 10000,
            "data": None,
            "msg": None
        })

# class CourseView(APIView):
#     '''课程'''
#     def get(self,request,*args,**kwargs):
#         print(args,kwargs)
#         pk = kwargs.get('pk')
#         print(pk,'-----')
#         if pk:
#             print(kwargs.get('pk'))
#             course_obj = models.Course.objects.filter(pk=pk).first()
#             print(course_obj.name)
#             ret = {
#                 'title': course_obj.name,
#                 'summary': course_obj.coursedetail.video_brief_link
#                 # 'summary':'欢迎大家来报名'
#             }
#         else:
#             # 查出所有的课程
#             ret = {'code': 1000, 'courseList': []}
#             course_obj = models.Course.objects.all()
#             for item in course_obj:
#                 d = {'name': item.name, 'id': item.id}
#                 ret['courseList'].append(d)
#         response= JsonResponse(ret)
#         response['Access-Control-Allow-Origin'] = '*'
#         return response

class DegreeView(APIView):
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
        return JsonResponse(res)

    def options(self, request, *args, **kwargs):
        return JsonResponse({
            "state": 10000,
            "data": None,
            "msg": None
        })
