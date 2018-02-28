
from django.http import JsonResponse
from rest_framework.views import APIView

from api.utils import my_serializers as my_seri
from . import models


class LoginView(APIView):
    """登录API"""
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
                ser = my_seri.CourseQuestionSerializer(instance=course_obj)
            else:
                ser = my_seri.CourseSerializer(instance=course_obj)
        else:
            course_list = models.Course.objects.all()
            ser = my_seri.CourseSerializer(instance=course_list, many=True)
        res["data"] = ser.data
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

