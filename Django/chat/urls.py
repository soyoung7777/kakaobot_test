from django.conf.urls import url
from . import views
from django.urls import path

urlpatterns = [
	url(r'^keyboard/',views.keyboard),
	url(r'^message',views.message),
	#url(r'^$',views.index),
	url(r'^index/(?P<pk>.+)/$',views.index, name='index'),
	path('',views.index, name='index')
	url(r'^pathFind/(?P<pk>.+)/$',views.detail_pathFind, name='pathFind'),
	path('',views.detail_pathFind, name='pathFind')
]
