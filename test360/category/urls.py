from django.conf.urls import url

from . import views

app_name = 'category'

urlpatterns = [
    url(r'^$', views.index, name='index'),
    url(r'^(?P<category_id>[0-9]+)/$', views.detail, name='detail'),
    url(r'^(?P<category_id>[0-9]+)/delete/$', views.delete, name='delete'),
]
