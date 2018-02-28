from rest_framework.serializers import ModelSerializer
from rest_framework import serializers
from .. import models
class CourseSerializer(ModelSerializer):
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
        return CourseDetailSerializer(detail_obj).data

class CourseDetailSerializer(ModelSerializer):
    price = serializers.SerializerMethodField()

    class Meta:
        model = models.CourseDetail
        fields = '__all__'
        # exclude = ["course"]
        depth = 2

    def get_price(self, obj):  #obj是CourseDetail对象
        return PricePolicySerializer(obj.course.price_policy.all(), many=True).data

class CourseChapterSerializer(ModelSerializer):
    course_chapters = serializers.CharField(source="coursechapters")

    class Meta:
        model = models.Course
        fields = '__all__'
        depth = 2

class CourseQuestionSerializer(ModelSerializer):
    class Meta:
        model = models.OftenAskedQuestion
        fields = ['question','answer']
        depth = 2

class PricePolicySerializer(ModelSerializer):
    valid_period = serializers.SerializerMethodField()

    class Meta:
        model = models.PricePolicy
        fields = '__all__'
        depth = 2

    def get_valid_period(self, obj):
        return obj.get_valid_period_display()

class DegreeCourseSerializer(ModelSerializer):
    class Meta:
        model = models.DegreeCourse
        fields = "__all__"
        depth = 2


