import json
import redis
import time
import hashlib

from django.core.exceptions import ObjectDoesNotExist
from django.http import JsonResponse
from django.conf import settings
from django.db import transaction

from rest_framework.views import APIView

from api import models
from api.utils.auth.auth_view import AuthForView
from api.utils.redis_pool import POOL
from api.utils.exceptions import *
from api.utils.more_data_type import ResData

# 链接redis
CONN = redis.Redis(connection_pool=POOL)


class ShoppingCartView(AuthForView, APIView):
    """
    购物车操作
    """

    def get(self, request, *args, **kwargs):
        try:
            cart = json.loads(CONN.hget(settings.SHOPPING_CART_KEY, request.user.id).decode("utf-8"))
        except AttributeError:
            # 用户第一次打开购物车
            cart = {}

        return JsonResponse(ResData(data=cart).__dict__)

    def post(self, request, *args, **kwargs):
        """
        请求体数据：
        {
            course_id: 1,
            price_policy_id: 2,
        }
        """
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


class SettlementListView(AuthForView, APIView):
    """
    结算清单，根据请求体数据从购物车获取商品，生成结算清单
    """

    def get(self, request, *args, **kwargs):
        try:
            res = ResData(data=json.loads(CONN.hget(settings.SETTLEMENT_LIST_KEY, request.user.id).decode("utf-8")))
        except AttributeError:
            res = ResData(state_code=40000, msg="尚未购买任何商品")
        return JsonResponse(res.__dict__)

    def patch(self, request, *args, **kwargs):
        """
        请求体数据:
            修改某课程的优惠卷
                {
                    course_id: 1,
                    coupon_record_id: 1,
                }
            修改全站优惠卷
                {
                    coupon_record_id: 8
                }
        """
        try:
            course_id = request.data.get("course_id")
            coupon_record_id = request.data.get("coupon_record_id")

            try:
                sl_data = json.loads(CONN.hget(settings.SETTLEMENT_LIST_KEY, request.user.id).decode("utf-8"))
            except AttributeError:
                return JsonResponse(ResData(state_code=40000, msg="非法提交").__dict__)
            if not course_id:
                # 修改全站优惠卷
                # 校验优惠卷是否存在
                flag = False
                for coupon in sl_data["global_coupon_list"]:
                    if coupon["id"] == coupon_record_id:
                        flag = True
                if not flag:
                    raise CouponDoesNotExist
                else:
                    sl_data["choose_coupon_id"] = coupon_record_id
            else:
                # 修改某课程优惠卷
                # 校验课程、优惠卷是否存在
                for item in sl_data["course_list"]:
                    if item["course_id"] == course_id:
                        for coupon in item["coupon_list"]:
                            if coupon["id"] == coupon_record_id:
                                item["choose_coupon_id"] = coupon_record_id
                                break
                        else:
                            raise CouponDoesNotExist
                        break
                else:
                    raise CourseDoesNotExist
            CONN.hset(settings.SETTLEMENT_LIST_KEY, request.user.id, json.dumps(sl_data))
            res = ResData(msg="更新成功")
        except CouponDoesNotExist:
            res = ResData(state_code=40000, msg="非法提交，不存在的优惠卷")
        except CourseDoesNotExist:
            res = ResData(state_code=40000, msg="非法提交，不存在的课程")
        # except Exception as e:
        #     print(e)
        #     res = ResData(state_code=40000, msg="提交错误，请检查数据")

        return JsonResponse(res.__dict__)


class OrderView(AuthForView, APIView):
    """
    订单操作
    """

    def post(self, request, *args, **kwargs):
        """
        从结算清单获取数据，计算价格，新增订单
        """
        try:
            sl_data = json.loads(CONN.hget(settings.SETTLEMENT_LIST_KEY, request.user.id).decode("utf-8"))
        except AttributeError:
            return JsonResponse(ResData(state_code=40000, msg="尚未购买任何商品").__dict__)

        def coupon_is_valid(coupon_record):
            """
            检验优惠卷是否有效

            :param coupon_record: 用户领取的单张优惠卷
            :return: 是否有效
            """
            now = time.time()

            flag = False
            # 检查优惠卷是否处于可使用期限，优惠卷都有使用区段，如双十一当天可用
            valid_begin_date = time.mktime(coupon_record.coupon.valid_begin_date.timetuple())
            valid_end_date = time.mktime(coupon_record.coupon.valid_end_date.timetuple())
            if (now > valid_begin_date) and (now < valid_end_date):
                # 检查优惠卷是否过期，优惠卷从被领取的时候有一个有效期，如7天
                if coupon_record.coupon.coupon_valid_days:
                    if now < (
                                time.mktime(coupon_record.get_time.timetuple())
                                + int(coupon_record.coupon.coupon_valid_days) * 86400):
                        flag = True
                else:
                    flag = True
            return flag

        def calc_price(price, coupon_record):
            """
            计算优惠后的价格

            :param price: 原价
            :param coupon_record: 优惠卷
            :return: 优惠后的价格
            """
            coupon = coupon_record.coupon
            if coupon.coupon_type == 0:   # 通用卷
                price = price - coupon.money_equivalent_value
            elif coupon.coupon_type == 2:  # 折扣卷
                price = price * (coupon.off_percent/100)
            else:   # 满减卷
                # 原价达到最低消费则满减
                price = price - coupon.money_equivalent_value if price > coupon.minimum_consume else 0
            return price

        total_price = 0.0
        # 1. 计算每个课程使用优惠卷的价格
        for course in sl_data["course_list"]:
            course["new_price"] = course["price"]
            try:
                # 获取选择的优惠券
                coupon_record_obj = models.CouponRecord.objects.get(id=course["choose_coupon_id"])
                # 检查优惠卷是否过期
                if not coupon_is_valid(coupon_record_obj):
                    raise CouponExpired
                else:
                    # 根据优惠卷种类分类判断、计算，保留折后价格
                    course["new_price"] = calc_price(float(course["price"]), coupon_record_obj)
                    total_price += course["new_price"]
            except ObjectDoesNotExist:
                # 该课程未使用课程优惠卷
                total_price += course["new_price"]
            except CouponExpired:
                # 优惠卷已过期
                total_price += course["new_price"]

        # 2. 计算使用全站优惠卷后的价格
        try:
            # 获取选择的优惠券
            coupon_record_obj = models.CouponRecord.objects.get(id=sl_data["choose_coupon_id"])
            # 检查优惠卷是否过期
            if not coupon_is_valid(coupon_record_obj):
                raise CouponExpired
            else:
                # 根据优惠卷种类分类判断、计算
                total_price = calc_price(total_price, coupon_record_obj)
        except ObjectDoesNotExist:
            # 未使用全站优惠卷
            pass
        except CouponExpired:
            # 优惠卷已过期
            pass
        # 3. 使用贝里
        is_use_balance = False
        pay_price = total_price
        if request.data.get("is_use_balance"):
            balance = request.user.balance
            # 检测贝里是否足够
            if balance > total_price:
                with transaction.atomic():
                    request.user.balance = request.user.balance - total_price
                    request.user.save()
                is_use_balance = True
                pay_price = 0
            else:
                with transaction.atomic():
                    request.user.balance = 0
                    request.user.save()
                pay_price = total_price - request.user.balance

        # 4. 生成订单
        md5 = hashlib.md5()
        md5.update(("order" + str(time.time())).encode("utf-8"))
        order_number = md5.hexdigest()

        with transaction.atomic():
            order_obj = models.Order.objects.create(
                payment_type=request.data.get("payment_type", 1) if not is_use_balance else 3,
                order_number=order_number,
                account=request.user,
                actual_amount=total_price,
                status=1
            )
            course_list = models.Course.objects.filter(id__in=[d["course_id"] for d in sl_data["course_list"]])
            # 生成订单详细
            for course in sl_data["course_list"]:
                models.OrderDetail.objects.create(
                    order=order_obj,
                    content_object=course_list.get(id=course["course_id"]),
                    original_price=course["price"],
                    price=course["new_price"],
                    valid_period_display=course["valid_period"],
                    valid_period=300
                )

            # valid_period=course["valid_period_num"]     # TODO： 更改结算页面redis数据

        return JsonResponse(ResData(msg=total_price).__dict__)


