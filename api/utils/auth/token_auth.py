from rest_framework.authentication import  BaseAuthentication
from  rest_framework.authentication import  get_authorization_header
from  django.utils.translation import  ugettext_lazy as  _
from  rest_framework import  HTTP_HEADER_ENCODING,exceptions
class  LuffyTokenAuthentication(BaseAuthentication):
    keyword='Token'
    def authenticate(self, request):
        token=request.query_params.get('token')
        if not token:
            raise exceptions.AuthenticationFailed('验证失败')
        return  self.authenticate_credetials(token)
    def authenticate_credetials(self, token):
        from api.models import  UserAuthToken
        try:
            token_obj=UserAuthToken.objects.select_related('user').get(token=token)
        except Exception as e:
            raise  exceptions.AuthenticationFailed(_('Invalid Tokne'))
        return  (token_obj.user,token_obj)


