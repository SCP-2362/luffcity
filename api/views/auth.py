from django.http import JsonResponse
from rest_framework.views import APIView
from .. import models


class LoginView(APIView):
    """登录API"""

    def post(self, request, *args, **kwargs):
        res = {
            "state": 10000,
            "data": None,
            "msg": None,
        }
        try:
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

                res["data"] = {
                    "username": username,
                    "token": user.userauthtoken.token
                }
            else:
                res["state"] = 40000,
                res["msg"] = "用户名或密码错误"
        except Exception as e:
            res["state"] = 40000
            res["msg"] = "出错啦！"
        return JsonResponse(res)

    def options(self, request, *args, **kwargs):
        return JsonResponse({
            "state": 10000,
            "data": None,
            "msg": None
        })

