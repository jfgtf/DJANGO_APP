"""ecommerce_project URL Configuration

The `urlpatterns` list routes URLs to views. For more information please see:
    https://docs.djangoproject.com/en/4.0/topics/http/urls/
Examples:
Function views
    1. Add an import:  from my_app import views
    2. Add a URL to urlpatterns:  path('', views.home, name='home')
Class-based views
    1. Add an import:  from other_app.views import Home
    2. Add a URL to urlpatterns:  path('', Home.as_view(), name='home')
Including another URLconf
    1. Import the include() function: from django.urls import include, path
    2. Add a URL to urlpatterns:  path('blog/', include('blog.urls'))
"""
from django.contrib import admin
from django.urls import path
from ecommerce_app import views

urlpatterns = [
    path("admin/", admin.site.urls),
    path(
        "products/create/",
        views.ProductCreate.as_view(),
        name="product-create",
    ),
    path("products/", views.ProductList.as_view(), name="product-list"),
    path(
        "products/<int:pk>/",
        views.ProductDetail.as_view(),
        name="product-detail",
    ),
    path("orders/", views.OrderList.as_view(), name="order-list"),
    path("orders/<int:pk>/", views.OrderDetail.as_view(), name="order-detail"),
    path(
        "place-order/", views.OrderPlacement.as_view(), name="order-placement"
    ),
    path(
        "top-ordered-products/",
        views.TopOrderedProducts.as_view(),
        name="top-ordered-products",
    ),
    path("categories/", views.CategoryList.as_view(), name="category-list"),
    path(
        "categories/create/",
        views.CategoryCreate.as_view(),
        name="category-create",
    ),
    path("users/create/", views.UserCreate.as_view(), name="user-create"),
    path("users/", views.UserList.as_view(), name="user-list"),
]
