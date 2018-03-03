from api import models
from rest_framework import serializers
class OrderSerialize(serializers.ModelSerializer):
    order_detail = serializers.SerializerMethodField()
    status = serializers.SerializerMethodField()
    #优惠
    #抵扣
    class Meta:
        model = models.Order
        fields = ['order_number','date','order_detail','status']

    def get_order_detail(self,obj):
        order_detail_list = obj.orderdetail_set.all()
        data_list = []
        for item in order_detail_list:
            data_list.append({
                'id':item.id,
                'original_price':item.original_price,
                'valid_period_display':item.valid_period_display,
                'course_img':item.content_object.course_img,
                'course_name':item.content_object.name,

            })
            print(item.content_object.course_img,'++++++++')
            print(item.content_object.name,'++++++++')
        return data_list


    def get_status(self,obj):
        return obj.get_status_display()