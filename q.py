import json

d = {
    "course_list": [
        {
            "course_id":1,
            "course_name": "python初级开发21天",
            "course_img": "/img/1.png",
            "valid_period": "一个月",
            "price":199,
            "coupon_list": [
                {"id": 1, "title": "通用卷，可抵50元", "is_active": True},
                {"id": 2, "title": "折扣卷，7.9折", "is_active": True},
                {"id": 3, "title": "满减卷，满199减49", "is_active": True},
            ],
            "choose_coupon_id": 1
        },
        {
            "course_id":2,
            "course_name": "django开发",
            "course_img": "/img/1.png",
            "valid_period": "一个月",
            "price":1999,
            "coupon_list": [],
            "choose_coupon_id": None
        }
    ],
    "global_coupon_list": [
        {"id": 4, "title": "通用卷，可抵500元", "is_active": True},
        {"id": 5, "title": "折扣卷，7.9折", "is_active": True},
        {"id": 6, "title": "满减卷，满1999减600", "is_active": True},
    ],
    "choose_coupon_id": None
}

print(json.dumps(d))
'{"course_list": [{"course_id": 1, "course_name": "python\u521d\u7ea7\u5f00\u53d121\u5929", "course_img": "/img/1.png", "valid_period": "\u4e00\u4e2a\u6708", "price": 199, "coupon_list": [{"id": 1, "title": "\u901a\u7528\u5377\uff0c\u53ef\u62b550\u5143", "is_active": true}, {"id": 2, "title": "\u6298\u6263\u5377\uff0c7.9\u6298", "is_active": true}, {"id": 3, "title": "\u6ee1\u51cf\u5377\uff0c\u6ee1199\u51cf49", "is_active": true}], "choose_coupon_id": 1}, {"course_id": 2, "course_name": "django\u5f00\u53d1", "course_img": "/img/1.png", "valid_period": "\u4e00\u4e2a\u6708", "price": 1999, "coupon_list": [], "choose_coupon_id": null}], "global_coupon_list": [{"id": 4, "title": "\u901a\u7528\u5377\uff0c\u53ef\u62b5500\u5143", "is_active": true}, {"id": 5, "title": "\u6298\u6263\u5377\uff0c7.9\u6298", "is_active": true}, {"id": 6, "title": "\u6ee1\u51cf\u5377\uff0c\u6ee11999\u51cf600", "is_active": true}], "choose_coupon_id": null}'




