from rest_framework.views import  APIView
from  rest_framework.response import Response
from api.utils.auth.auth_view import  AuthForView
from api.utils.redis_pool import POOL
from api.utils.more_data_type import ResData
from rest_framework.response import Response
from django.http import JsonResponse
from api import  models
from api.utils.more_data_type import ResData
import  json
from   django.conf import  settings
import  redis

CONN=redis.Redis(connection_pool=POOL)


class SettlementListView(AuthForView, APIView):
  def post(self,request,*args,**kwargs):
      # res = ResData(state_code=10000)
      # 1获取课程id和价格策略id
      course_list_id = request.data.get("course_id")#获取所有传过来的课程id
      # print(course_list_id)
      price_policy_id = request.data.get("price_policy_id")
      if   price_policy_id:
          #如果没有价格策略
          pass
      else:
          cart = json.loads(CONN.hget(settings.SHOPPING_CART_KEY, request.user.id).decode("utf-8"))#获取货物车里面的信息
          # print(cart)
          #判断传来的课程id是不是存在购物车里
          flag=False
          course_list=[]
          for id  in course_list_id:
               if str(id) in cart:
                     flag=True
                     #获取课程的优惠券
                     course_obj=models.Course.objects.get(id=int(id))
                     coupon_list = []
                     #取出课程的周期和价格
                     for item in course_obj.coupon.all():
                         coupon_list.append({'id': item.id, 'type_name': item.name, 'type_id': item.coupon_type})
                     for item in cart[str(id)]['price_policy_list']:
                         if item['id']==cart[str(id)]['default_price_id']:
                             course_list.append(
                                 {'course_id': id, 'course_name': course_obj.name, 'course_img': course_obj.course_img,
                                  'valid_period': item['valid_period'], 'price': item['price'],
                                  'coupon_list': coupon_list})
                     # print(course_list)
                     account_obj=models.CouponRecord.objects.filter(account=request.user)
                     global_coupon_list=[]
                     for item in account_obj:
                        global_coupon_list.append({
                           'id':item.coupon.id,
                           'type_name':item.coupon.name,
                           'coupon_type':item.coupon.coupon_type,
                             })

          all_list = {
              'couser_list': course_list,
              'global_coupon_list':global_coupon_list,
              'choose_coupon_id':cart[str(id)]['default_price_id']
          }

          CONN.hset(settings.SETTLEMENT_LIST_KEY, request.user.id,json.dumps(all_list))#获取货物车里面的信息

          cart = json.loads(CONN.hget(settings.SETTLEMENT_LIST_KEY, request.user.id).decode("utf-8"))  #
      return  Response('设置成功')




