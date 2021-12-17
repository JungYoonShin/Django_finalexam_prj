from django.urls import path
from . import views

urlpatterns = [
    path('', views.landing),
    path('mypage/', views.mypage),
    path('about_company/', views.about_company),
]
