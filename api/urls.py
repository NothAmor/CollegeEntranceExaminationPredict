from django.urls import path

from . import views

urlpatterns = [
    path('spider', views.spider, name='spider'),
    path('predict', views.predict, name='predict'),
]