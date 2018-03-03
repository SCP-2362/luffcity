from collections import OrderedDict

from rest_framework.views import  APIView
from rest_framework.response import  Response
from api.utils.auth.auth_view import AuthForView
from api import models
from api.utils.more_data_type import ResData
from api.serializers.order import  OrderSerialize


class OrderView(AuthForView,APIView):
    def get(self,request,*args,**kwargs):
        ret = ResData()
        #获取订单日期和订单号
        try:
            order_list = models.Order.objects.all()
            ser = OrderSerialize(instance=order_list,many=True)
            for item in ser.data:
                item["date"] = item["date"][0:19]  #更换时间格式
            #获取订单详细
            ret.data = ser.data

        except Exception as e:
            print(e)
        return Response(ret.__dict__)