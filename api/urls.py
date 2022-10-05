from django.urls import path

from . import views

urlpatterns = [
    path('spider', views.spider, name='spider'),
    path('preview', views.preview, name='preview'),
]