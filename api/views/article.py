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
            result['data'] = ret.data
            return JsonResponse(result)
        except Exception as e:
            result['state'] = 40000
            result['msg'] = str(e)
            return JsonResponse(result)

    def post(self, request, *args, **kwargs):
        result = {
            "state": '',
            "data": '',
            "msg": None
        }
        try:
            pk = kwargs.get('pk')
            if pk:
                art_obj = models.Article.objects.filter(id=pk).update(agree_num=F('agree_num') + 1)
                art_obj = models.Article.objects.get(id=pk)
                ret = ArticleContentSerializer(instance=art_obj)

            else:
                pass
            result['state'] = 10000
            result['data'] = ret.data
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
            if pk:
                art_obj = models.Article.objects.filter(id=pk).update(collect_num=F('collect_num') + 1)
                art_obj = models.Article.objects.get(id=pk)
                ret = ArticleContentSerializer(instance=art_obj)
                print(art_obj.collect_num, '1')

            else:
                pass
            result['state'] = 10000
            result['data'] = ret.data
            return JsonResponse(result)
        except Exception as e:
            result['state'] = 40000
            result['msg'] = str(e)
            return JsonResponse(result)