from django.conf.urls import url
from . import views

urlpatterns=[
    url(r'^$',views.welcome, name = 'welcome'),
    # url(r'^$',views.news_today,name='newsToday'),
]