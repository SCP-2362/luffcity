from rest_framework.response import Response
from rest_framework.views import APIView

from api import models
from api.serializers.dregeeregisterform import DrfSerialize
from api.utils.auth.auth_view import AuthForView


class DegreeRegistFormView(AuthForView, APIView):
    def get(self, request, *args, **kwargs):
        # 获取数据并且在页面上渲染，前端就不用写了
        drf_list = models.DegreeRegistrationForm.objects.all()
        ser = DrfSerialize(instance=drf_list, many=True)
        return Response(ser.data)

    def post(self, request, *args, **kwargs):
        ser = DrfSerialize(data=request.data, many=True)
        if ser.is_valid():
            print('验证成功', ser.validated_data)
        else:
            print('验证失败', ser.errors)
        return Response(ser.validated_data)
