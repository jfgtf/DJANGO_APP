from django.contrib import admin
from ecommerce_app.admin_mixins import AllFieldsListDisplayMixin
from ecommerce_app.models import Category, Product, UserProfile


@admin.register(Category)
class CategoryAdmin(AllFieldsListDisplayMixin, admin.ModelAdmin):
    class Meta:
        verbose_name = "Categories"
        verbose_name_plural = "Categories"


@admin.register(Product)
class ProductAdmin(AllFieldsListDisplayMixin, admin.ModelAdmin):
    pass


@admin.register(UserProfile)
class UserProfileAdmin(AllFieldsListDisplayMixin, admin.ModelAdmin):
    pass


# Register your models here.
