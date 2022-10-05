from django.urls import path

from . import views

urlpatterns = [
    path('', views.index, name='index'),
    path('spider', views.spider, name='spider'),
    path('preview', views.preview, name='preview'),
    path('minimal', views.minimal, name='minimal'),
]