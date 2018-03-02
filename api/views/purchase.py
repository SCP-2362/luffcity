import json
import redis

from django.core.exceptions import ObjectDoesNotExist
from django.http import JsonResponse
from django.conf import settings

from rest_framework.views import APIView

from api import models
from api.utils.auth.auth_view import AuthForView
from api.utils.redis_pool import POOL
from api.utils.exceptions import PricePolicyDoesNotExist
from api.utils.more_data_type import ResData

# 链接redis
CONN = redis.Redis(connection_pool=POOL)


class ShoppingCartView(AuthForView, APIView):

    def get(self, request, *args, **kwargs):
        try:
            cart = json.loads(CONN.hget(settings.SHOPPING_CART_KEY, request.user.id).decode("utf-8"))
        except AttributeError:
            # 用户第一次打开购物车
            cart = {}

        return JsonResponse(ResData(data=cart).__dict__)

    def post(self, request, *args, **kwargs):
        res = ResData(state_code=10000)
        # 传入课程ID和价格策略ID
        course_id = request.data.get("course_id")
        price_policy_id = request.data.get("price_policy_id")
        try:
            # 通过课程对象，获取所有的价格策略
            course_obj = models.Course.objects.get(pk=course_id)
            price_list = course_obj.price_policy.all()
            goods_info = {
                "price_policy_list": [
                    {"id": p.id, "price": p.price, "valid_period": p.get_valid_period_display()}
                    for p in price_list],
                "default_price_id": price_policy_id,
                "course_id": course_obj.id,
                "course_name": course_obj.name,
                "course_pic": course_obj.id,

            }
            # 检测传入的价格策略是否符合当前课程
            if float(price_policy_id) not in [obj.id for obj in price_list]:
                raise PricePolicyDoesNotExist("非法提交！")
            else:
                # 获取购物车
                try:
                    cart = json.loads(CONN.hget(settings.SHOPPING_CART_KEY, request.user.id).decode("utf-8"))
                except AttributeError:
                    # 第一次向购物车添加，无法获取到值
                    cart = {}

                if str(course_obj.id) in cart:
                    res.msg = "更新购物车成功！"
                else:
                    res.msg = "加入购物车成功！"

                cart[course_obj.id] = goods_info
                CONN.hset(settings.SHOPPING_CART_KEY, request.user.id, json.dumps(cart))
                res.data = cart

        except ObjectDoesNotExist:
            res = ResData(state_code=40004, msg="课程不存在！")

        except PricePolicyDoesNotExist as e:
            res = ResData(state_code=40004, msg="非法操作，价格不存在！")

        # except Exception as e:
        #     res["state"] = 40000
        #     res["msg"] = "服务器错误"

        return JsonResponse(res.__dict__)

    def delete(self, request, *args, **kwargs):
        res = {
            "state": 10000,
            "data": None,
            "msg": None
        }
        course_id = request.data.get("course_id")
        try:
            cart = json.loads(CONN.hget(settings.SHOPPING_CART_KEY, request.user.id).decode("utf-8"))
            cart.pop(str(course_id))
            CONN.hset(settings.SHOPPING_CART_KEY, request.user.id, json.dumps(cart))
            res["data"] = cart
        except AttributeError:
            # 用户第一次打开购物车，但是第一次打开购物车不可能走到这一步
            res["state"] = 40000
            res["msg"] = "非法操作，请检查数据"
        except KeyError:
            # 购物车已空或者删除不存在的商品，正常流程不会走到这一步
            res["state"] = 40000
            res["msg"] = "非法操作，请检查数据"

        return JsonResponse(res)

    def patch(self, request, *args, **kwargs):
        # 局部更新与post功能重复，建议直接发post请求

        res = ResData(msg="局部更新与post功能重复，请直接发post请求")
        return JsonResponse(res)

    def options(self, request, *args, **kwargs):
        return JsonResponse({
            "state": 10000,
            "data": None,
            "msg": None
        })
