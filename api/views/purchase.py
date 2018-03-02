from django.http import JsonResponse
from rest_framework.views import APIView

from api.utils.auth_token import MyTokenAuth
from .. import models


class ShoppingCartView(APIView):
    authentication_classes = [MyTokenAuth, ]

    def get(self, request, *args, **kwargs):
        res = {
            "state": 10000,
            "data": None,
            "msg": None
        }

        return JsonResponse(res)

    def post(self, request, *args, **kwargs):
        res = {
            "state": 10000,
            "data": None,
            "msg": None
        }

        return JsonResponse(res)

    def options(self, request, *args, **kwargs):
        return JsonResponse({
            "state": 10000,
            "data": None,
            "msg": None
        })
