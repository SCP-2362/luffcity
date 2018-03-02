
from rest_framework import serializers


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