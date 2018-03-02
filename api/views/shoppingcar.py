from rest_framework.views import APIView
from api.utils.auth.api_view import AuthAPIView
from rest_framework.response import Response
from django.core.exceptions import ObjectDoesNotExist
from api.utils.exception import PricePolicyDoesNotExist
from django.http import JsonResponse
from  api import models
from pool import POOL
import json
import redis
import  demjson

CONN = redis.Redis(connection_pool=POOL)


class ShoppingCarView(AuthAPIView, APIView):
    def get(self, request, *args, **kwargs):
        ret = {'code': 1000, 'msg': None,'data':None}
        data = CONN.hget('shopping_car', request.user.id)
        try:
          data = json.loads(data.decode('utf-8'))
          ret['data']=data
        except AttributeError as e:
            ret['code'] = 1005
            ret['msg'] = '没有课程'

        return Response(ret)
    def delete(self,request,*args, **kwargs):
        ret = {'code': 1000, 'msg': None}
        data = CONN.hget('shopping_car', request.user.id)
        data = json.loads(data.decode('utf-8'))
        course_id = request.data.get('cousrse_id')  # 获取值
        print(course_id)
        if str(course_id) not in data:
            ret['code']=1004
            ret['msg']='您选择的课程不存在'
        else:
            shopping_dict = CONN.hget('shopping_car', request.user.id)
            data = json.loads((shopping_dict.decode('utf-8')))
            data.pop(str(course_id))
            CONN.hset('shopping_car', request.user.id, json.dumps(data))
        return Response(ret)
    def patch(self,request,*args,**kwargs):
       return  Response('局部更新，可以直接使用post方法')
    def post(self, request, *args, **kwargs):
        ret = {'code': 1000, 'msg': None}
        try:
            course_id = request.data.get('cousrse_id')  # 获取值
            price_policy_id = request.data.get('price_policy_id')
            # 1.获取课程
            course_obj = models.Course.objects.get(id=course_id)
            price_policy_list = []
            flag = False
            price_policy_objs = course_obj.price_policy.all()
            for item in price_policy_objs:
                if item.id == price_policy_id:
                    flag = True
                price_policy_list.append(
                    {'id': item.id, 'valid_period': item.get_valid_period_display(), 'price': item.price})
            # print(price_policy_list)
            if not flag:
                raise PricePolicyDoesNotExist()
            course_dict = {
                'id': str(course_obj.id),
                'img': course_obj.course_img,
                'title': course_obj.name,
                'price_policy_list': price_policy_list,
                'default_policy_id': price_policy_id
            }
            shopping_dict = CONN.hget('shopping_car', request.user.id)
            if not shopping_dict:
                data = {course_obj.id: course_dict}
            else:
                data = json.loads((shopping_dict.decode('utf-8')))  # 先解码，然后在loads变成字典格式的
                data[course_obj.id] = course_dict

            print(data, type(data))
            CONN.hset('shopping_car', request.user.id, json.dumps(data))


        except ObjectDoesNotExist as e:
            ret['code'] = 1001
            ret['msg'] = '课程不存在'
        except PricePolicyDoesNotExist as e:
            ret['code'] = 1002
            ret['msg'] = '价格不存在'
        except Exception as e:
            ret['code'] = 1003
            ret['msg'] = "添加购物车异常"

        return Response(ret)
