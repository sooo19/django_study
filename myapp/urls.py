from django.urls import path
from myapp import views

# 사용자가 아래와 같은 경로들로 접속했을 시, views.py로 전달
urlpatterns = [
    path('', views.index),
    path('create/', views.create),
    path('read/<id>/', views.read)

]
