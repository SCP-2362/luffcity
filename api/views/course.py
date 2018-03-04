from django.http import JsonResponse
from rest_framework.views import APIView

from api.serializers.course import *
from .. import models


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
        # try:
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
                    ser = CourseDetailModelSerializer(instance=detail_obj)
                else:
                    wrong_res["msg"] = "暂无课程详细"
                    return JsonResponse(wrong_res)
            elif request.query_params.get("data_type") == "chapters":
                chapter_list = course_obj.coursechapters.all()
                ser = CourseChapterModelSerializer(instance=chapter_list, many=True)
            elif request.query_params.get("data_type") == "question":
                # 根据课程去找问题
                # questiion_list = course_obj.oftenaskedquestion_set.all()
                from django.contrib.contenttypes.models import ContentType
                print(course_obj._meta.model_name, '表名')
                ct_id = ContentType.objects.filter(app_label='api', model=course_obj._meta.model_name).first().id
                o_list = models.OftenAskedQuestion.objects.filter(content_type_id=ct_id, object_id=course_obj.id)
                print(o_list)
                ser = CourseQuestionModelSerializer(instance=o_list, many=True)
            else:
                ser = CourseModelSerializer(instance=course_obj)
        else:
            # 课程列表
            course_list = models.Course.objects.all()
            ser = CourseModelSerializer(instance=course_list, many=True)
        res["data"] = ser.data
        # except Exception as e:
        #     print(e)
        #     res["state"] = 40000
        #     res["msg"] = "出错啦！"
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
        # try:
        if kwargs.get("pk"):
            degree_obj = models.DegreeCourse.objects.filter(pk=kwargs.get("pk")).first()
            if request.query_params.get("data_type") == "detail":
                pass
            else:
                ser = DegreeCourseModelSerializer(degree_obj)
        else:
            degree_list = models.DegreeCourse.objects.all()
            ser = DegreeCourseModelSerializer(instance=degree_list, many=True)
        res["data"] = ser.data
        # except Exception as e:
        #     res["state"] = 40000
        #     res["msg"] = "出错啦！"
        return JsonResponse(res)

    def options(self, request, *args, **kwargs):
        return JsonResponse({
            "state": 10000,
            "data": None,
            "msg": None
        })
