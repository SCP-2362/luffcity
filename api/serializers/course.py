from rest_framework import serializers
from .. import models

from .price import *


class CourseModelSerializer(serializers.ModelSerializer):
    level = serializers.SerializerMethodField()
    detail = serializers.SerializerMethodField()

    class Meta:
        model = models.Course
        fields = '__all__'
        depth = 2

    def get_level(self, obj):
        return obj.get_level_display()

    def get_detail(self, obj):
        detail_obj = models.CourseDetail.objects.filter(course=obj).first()
        return CourseDetailModelSerializer(detail_obj).data


class CourseDetailModelSerializer(serializers.ModelSerializer):
    price = serializers.SerializerMethodField()
    outline = serializers.SerializerMethodField()

    class Meta:
        model = models.CourseDetail
        fields = '__all__'
        # exclude = ["course"]
        depth = 2

    def get_price(self, obj):
        return PricePolicyModelSerializer(obj.course.price_policy.all(), many=True).data

    def get_outline(self, obj):
        return CourseOutlineModelSerializer(obj.courseoutline_set.all(), many=True).data


class CourseChapterModelSerializer(serializers.ModelSerializer):
    coursesections = serializers.SerializerMethodField()

    class Meta:
        model = models.CourseChapter
        fields = '__all__'
        depth = 1

    def get_coursesections(self, obj):
        return CourseSectionModelSerializer(obj.coursesections.all(), many=True).data


class CourseQuestionModelSerializer(serializers.ModelSerializer):

    class Meta:
        model = models.OftenAskedQuestion
        fields = '__all__'
        depth = 2


class CourseOutlineModelSerializer(serializers.ModelSerializer):
    class Meta:
        model = models.CourseOutline
        fields = "__all__"
        depth = 2


class CourseSectionModelSerializer(serializers.ModelSerializer):
    class Meta:
        model = models.CourseSection
        fields = "__all__"
        depth = 1


class DegreeCourseModelSerializer(serializers.ModelSerializer):
    class Meta:
        model = models.DegreeCourse
        fields = "__all__"
        depth = 2