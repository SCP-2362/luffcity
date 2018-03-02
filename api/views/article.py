from django.http import JsonResponse
from django.db.models import F

from rest_framework.views import APIView

from api.serializers.article import *
from .. import models


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
                ret = ArticleContentSerializer(instance=art_obj)
            else:
                article = models.Article.objects.all()
                ret = ArticleSerializer(instance=article, many=True)
                ret.is_valid()
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
                ret = ArticleContentSerializer(instance=art_obj)
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
                ret = ArticleContentSerializer(instance=art_obj)
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