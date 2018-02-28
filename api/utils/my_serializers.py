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
    outline = serializers.SerializerMethodField()

    class Meta:
        model = models.CourseDetail
        fields = '__all__'
        # exclude = ["course"]
        depth = 2

    def get_price(self, obj):
        return PricePolicySerializer(obj.course.price_policy.all(), many=True).data

    def get_outline(self, obj):
        return CourseOutlineSerializer(obj.courseoutline_set.all(), many=True).data


class CourseChapterSerializer(ModelSerializer):
    coursesections = serializers.SerializerMethodField()

    class Meta:
        model = models.CourseChapter
        fields = '__all__'
        depth = 1

    def get_coursesections(self, obj):
        return CourseSectionSerializer(obj.coursesections.all(), many=True).data


class CourseQuestionSerializer(ModelSerializer):
    course_question = serializers.CharField(source="coursedetail.oftenaskedquestion")

    class Meta:
        model = models.Course
        fields = '__all__'
        depth = 2


class PricePolicySerializer(ModelSerializer):
    valid_period = serializers.SerializerMethodField()

    class Meta:
        model = models.PricePolicy
        fields = '__all__'
        depth = 2

    def get_valid_period(self, obj):
        return obj.get_valid_period_display()


class CourseOutlineSerializer(ModelSerializer):
    class Meta:
        model = models.CourseOutline
        fields = "__all__"
        depth = 2


class CourseSectionSerializer(ModelSerializer):
    class Meta:
        model = models.CourseSection
        fields = "__all__"
        depth = 1


class DegreeCourseSerializer(ModelSerializer):
    class Meta:
        model = models.DegreeCourse
        fields = "__all__"
        depth = 2


class ArticleSerializer(serializers.Serializer):
    pk = serializers.CharField()
    title = serializers.CharField()       #标题
    source = serializers.CharField(source='source.name')   #来源
    brief = serializers.CharField()   # 摘要
    date = serializers.CharField() #日期
    comment_num = serializers.CharField() #评论数
    agree_num = serializers.CharField()
    view_num = serializers.CharField() #观看数
    collect_num = serializers.CharField() #收藏数


class ArticleContentSerializer(serializers.Serializer):
    title = serializers.CharField()  # 标题
    agree_num = serializers.CharField()
    content = serializers.CharField() #文章详情
    collect_num = serializers.CharField()  # 收藏数
