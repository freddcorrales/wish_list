from django.conf.urls import url, include
from . import views

urlpatterns = [
    url(r'^dashboard$', views.dashboard),
    url(r'^wish_items/create$', views.add_page),
    url(r'^data$', views.data),
    url(r'^join/(?P<itemid>\d+)$', views.join),
    url(r'^wish_items/(?P<itemid>\d+)$', views.wish_items),
    url(r'^delete/(?P<itemid>\d+)$', views.delete),
]