from django.conf.urls import url
from . import views
from django.urls import path

urlpatterns = [
	url(r'^keyboard/',views.keyboard),
	url(r'^message',views.message),
	url(r'^$',views.index),
	path('',views.index, name='index')
]
