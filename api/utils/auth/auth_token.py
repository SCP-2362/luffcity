import datetime

from rest_framework.authentication import BaseAuthentication
from rest_framework.exceptions import AuthenticationFailed

from api import models


class LuffyCityTokenAuth(BaseAuthentication):
    keyword = "token"
    model = models.UserAuthToken
    valid_period = 86400000  # 86400000毫秒=24小时
    # valid_period = 100000            # 86400000毫秒=24小时

    res = {
        "state": 40000,
        "data": {
            "back_url": None,
            # "auth_url": None
        },
        "msg": None
    }

    def authenticate(self, request):
        self.res["data"]["back_url"] = request.path_info
        token = request.query_params.get(self.keyword, None)
        if not token:
            self.res["msg"] = "请登录后访问"
            raise AuthenticationFailed(self.res)

        auth = self.model.objects.filter(token=token).first()
        if not auth:
            self.res["msg"] = "认证失败，请重新登录！"
            raise AuthenticationFailed(self.res)

        token_exist_period = self.get_token_exist_period(auth)
        if token_exist_period > self.valid_period:
            self.res["msg"] = "认证已过期，请重新登录！"
            raise AuthenticationFailed(self.res)

        return auth.user, auth

    def get_token_exist_period(self, auth):
        now = datetime.datetime.now()
        return now.timestamp() - auth.created.timestamp()
