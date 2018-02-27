import datetime

from django.http import JsonResponse
from rest_framework.views import APIView

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
