from django.contrib.auth.models import User
from django.db import models


class Category(models.Model):
    name = models.CharField(max_length=100)


class Product(models.Model):
    name = models.CharField(max_length=100)
    description = models.TextField()
    price = models.DecimalField(max_digits=10, decimal_places=2)
    category = models.ForeignKey(Category, on_delete=models.CASCADE)
    image = models.ImageField(upload_to="assets/images/")
    thumbnail = models.ImageField(upload_to="assets/thumbnails/")


class Order(models.Model):
    customer = models.ForeignKey(
        "ecommerce_app.UserProfile", on_delete=models.CASCADE
    )
    shipping_address = models.TextField()
    products = models.ManyToManyField(Product, through="OrderProduct")
    order_date = models.DateTimeField(auto_now_add=True)
    payment_due_date = models.DateTimeField()


class OrderProduct(models.Model):
    product = models.ForeignKey(Product, on_delete=models.CASCADE)
    order = models.ForeignKey(Order, on_delete=models.CASCADE)
    quantity = models.PositiveIntegerField()


class UserProfile(models.Model):
    class RoleChoice(models.TextChoices):
        CLIENT = "Client", "Client"
        SELLER = "Seller", "Seller"

    user = models.OneToOneField(User, null=False, on_delete=models.CASCADE)
    role = models.CharField(
        max_length=30, choices=RoleChoice.choices, default=RoleChoice.CLIENT
    )
