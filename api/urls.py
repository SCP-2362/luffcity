from django.conf.urls import url
from . import views

urlpatterns = [
    url(r'^login/', views.LoginView.as_view()),
    url(r'^news/$', views.NewsView.as_view()),
    url(r'^news/(?P<pk>\d+)/$', views.NewsView.as_view()),
    url(r'^shoucang/(?P<pk>\d+)/$', views.NewsViewSC.as_view()),


]
