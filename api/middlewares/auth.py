from django.http import JsonResponse
from .base import MiddlewareMixin


class AuthMiddleware(MiddlewareMixin):

    def process_request(self, request):
        token = request.GET.get("token")
        if not token:
            return JsonResponse({
                "state": 30002,
                "data": {
                    "back_url": request.path_info
                },
                "msg": "请登录后访问！"
            })



