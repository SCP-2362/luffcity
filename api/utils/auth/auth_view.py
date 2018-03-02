from api.utils.auth.auth_token import LuffyCityTokenAuth


class AuthForView(object):
    authentication_classes = [LuffyCityTokenAuth, ]
