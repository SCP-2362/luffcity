
from django.http import JsonResponse
from rest_framework.views import APIView
from rest_framework.response import Response
from rest_framework import serializers
from api import models
from django.db.models import  F


class Article(serializers.Serializer):
    pk = serializers.CharField()
    title = serializers.CharField()       #标题
    source = serializers.CharField(source='source.name')   #来源
    brief = serializers.CharField()   # 摘要
    date = serializers.CharField() #日期
    comment_num = serializers.CharField() #评论数
    agree_num = serializers.CharField()
    view_num = serializers.CharField() #观看数
    collect_num = serializers.CharField() #收藏数


class ArticleContent(serializers.Serializer):
    title = serializers.CharField()  # 标题
    agree_num = serializers.CharField()
    content = serializers.CharField() #文章详情
    collect_num = serializers.CharField()  # 收藏数


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


class NewsView(APIView):
    def get(self,request, *args, **kwargs):
        result = {
            "state": '',
            "data": '',
            "msg": None
        }
        try:
            pk = kwargs.get('pk')
            if pk:
                art_obj = models.Article.objects.get(id=pk)
                ret = ArticleContent(instance=art_obj)
            else:
                article = models.Article.objects.all()
                print(type (article),'999999')
                ret = Article(instance=article,many=True)
            result['state'] = 10000
            result['data'] = ret.data
            return Response(result)
        except Exception as e:
            result['state'] = 40000
            result['msg'] = str(e)
            return Response(result)
    def post(self,request,*args,**kwargs):
        result = {
            "state": '',
            "data": '',
            "msg": None
        }
        try:
            pk = kwargs.get('pk')
            print(pk)
            if pk :
              art_obj = models.Article.objects.filter(id=pk).update(agree_num=F('agree_num')+1)
              art_obj = models.Article.objects.get(id=pk)
              ret = ArticleContent(instance=art_obj)
              print(art_obj.agree_num,'1')

            else:
                pass
            result['state'] = 10000
            result['data'] = ret.data
            return Response(result)
        except Exception as e:
            result['state'] = 40000
            result['msg'] = str(e)
            return Response(result)

class NewsViewSC(APIView):

            def post(self, request, *args, **kwargs):
                result = {
                    "state": '',
                    "data": '',
                    "msg": None
                }
                try:
                    pk = kwargs.get('pk')
                    print(pk)
                    if pk:
                        art_obj = models.Article.objects.filter(id=pk).update(collect_num=F('collect_num') + 1)
                        art_obj = models.Article.objects.get(id=pk)
                        ret = ArticleContent(instance=art_obj)
                        print(art_obj.collect_num, '1')

                    else:
                        pass
                    result['state'] = 10000
                    result['data'] = ret.data
                    return Response(result)
                except Exception as e:
                    result['state'] = 40000
                    result['msg'] = str(e)
                    return Response(result)


