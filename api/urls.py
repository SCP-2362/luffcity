from django.conf.urls import url

from api.views.article import *
from api.views.course import *
from api.views.auth import *
from api.views.order import *

from api.views.purchase import *
from api.views.pay import *
from api.views.degreeregistform import *



urlpatterns = [
    url(r'^login/$', LoginView.as_view()),

    url(r'^courses/$', CoursesView.as_view()),
    url(r'^courses/(?P<pk>\d+)\.json$', CoursesView.as_view()),

    url(r'^degrees/$', DegreeView.as_view()),
    url(r'^degrees/(?P<pk>\d+)\.json$', DegreeView.as_view()),
    url(r'^login/', LoginView.as_view()),

    url(r'^news/$', NewsView.as_view()),
    url(r'^news/(?P<pk>\d+)/$', NewsView.as_view()),
    url(r'^shoucang/(?P<pk>\d+)/$', NewsViewSC.as_view()),

    url(r'^shopping_cart/$', ShoppingCartView.as_view()),

    url(r'^order/$', OrderView.as_view()),  #订单
    url(r'^page1/$',Page1View.as_view()),  #去支付
    url(r'^page2/$',Page2View.as_view()),  #去支付

    url(r'^degreeregistform/$', DegreeRegistFormView.as_view()),  #学位课报名表




]
