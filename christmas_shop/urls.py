from django.urls import path
from . import views


urlpatterns = [
    path('', views.ProductList.as_view()),
    path('<int:pk>/', views.ProductDetail.as_view()),
    path('category/<str:slug>/', views.category_page),
    path('create_product/', views.ProductCreate.as_view()),
    path('update_post/<int:pk>/', views.ProductUpdate.as_view()),
]
