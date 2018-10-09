from django.conf.urls import url
from . import views
from django.conf import settings
from django.conf.urls.static import static

urlpatterns=[
    url(r'^$',views.welcome, name = 'welcome'),
    url(r'^signup/$', views.signup, name='signup'),
    url(r'^activate/(?P<uidb64>[0-9A-Za-z_\-]+)/(?P<token>[0-9A-Za-z]{1,13}-[0-9A-Za-z]{1,20})/$',
        views.activate, name='activate'),
    url(r'^search/', views.search_results, name='search_results'),
    url(r'^edit/', views.edit_profile, name='edit_profile'),
    url(r'^profile/$', views.profile, name = 'profile'),
    url(r'^post/', views.post_image, name='post_image'),
    url(r'^comment/(\d+)', views.comment, name='comment'),

]
if settings.DEBUG:
  urlpatterns += static(settings.MEDIA_URL, document_root=settings.MEDIA_ROOT)
