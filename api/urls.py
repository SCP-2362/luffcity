from django.conf.urls import url
from . import views

urlpatterns = [
    url(r'^login/$', views.LoginView.as_view()),

    url(r'^courses/$', views.CoursesView.as_view()),
    url(r'^courses/(?P<pk>\d+)\.json$', views.CoursesView.as_view()),

    url(r'^degrees/$', views.DegreeView.as_view()),
    url(r'^degrees/(?P<pk>\d+)\.json$', views.DegreeView.as_view()),
    url(r'^login/', views.LoginView.as_view()),

    url(r'^news/$', views.NewsView.as_view()),
    url(r'^news/(?P<pk>\d+)/$', views.NewsView.as_view()),
    url(r'^shoucang/(?P<pk>\d+)/$', views.NewsViewSC.as_view()),

]
