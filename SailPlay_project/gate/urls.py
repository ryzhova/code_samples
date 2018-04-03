from django.conf.urls import url

from . import views

app_name = 'gate'

urlpatterns = [
    url(r'^$', views.gate, name='gate'),
]
