from django.contrib import admin
from ecommerce_app.admin_mixins import AllFieldsListDisplayMixin
from ecommerce_app.models import (
    Category,
    Order,
    OrderProduct,
    Product,
    UserProfile,
)


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


@admin.register(Order)
class OrderAdmin(admin.ModelAdmin):
    list_display = (
        "user",
        "shipping_address",
        "get_products",
        "order_date",
        "payment_due_date",
    )

    @admin.display(description="products")
    def get_products(self, obj):
        return [products.name for products in obj.products.all()]


@admin.register(OrderProduct)
class OrderProductAdmin(AllFieldsListDisplayMixin, admin.ModelAdmin):
    pass


# Register your models here.
