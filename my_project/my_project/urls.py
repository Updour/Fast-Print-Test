# urls.py

from django.contrib import admin
from django.urls import path, get_resolver
from . import views
from .views import RegisterView, LoginView

urlpatterns = [
    path('admin/', admin.site.urls),
  
    # URL untuk Register
    path('api/register/', RegisterView.as_view(), name='register'),
    path('api/login/', LoginView.as_view(), name='login'),

   # URL untuk CRUD Produk
    path('api/produk/', views.produk_list, name='produk_list'),
    path('api/create/', views.produk_create, name='produk_create'),
    path('api/update/<int:id>/', views.produk_update, name='produk_update'),
    path('api/delete/<int:id>/', views.produk_delete, name='produk_delete'),

    # URL untuk Register dan Login
    path('api/register/', views.RegisterView.as_view(), name='register'),
    path('api/login/', views.LoginView.as_view(), name='login'),
]
