from django.contrib.auth.models import User
from django.db import models


class Category(models.Model):
    name = models.CharField(max_length=100)

    def __str__(self):
        return self.name


class Product(models.Model):
    name = models.CharField(max_length=100)
    description = models.TextField()
    price = models.DecimalField(max_digits=10, decimal_places=2)
    category = models.ForeignKey(Category, on_delete=models.CASCADE)
    image = models.ImageField(upload_to="assets/images/")
    thumbnail = models.ImageField(
        upload_to="assets/thumbnails/", blank=True, null=True
    )

    def __str__(self):
        return self.name


class Order(models.Model):
    user = models.ForeignKey(
        "ecommerce_app.UserProfile", on_delete=models.CASCADE
    )
    shipping_address = models.TextField()
    products = models.ManyToManyField(
        Product, through="ecommerce_app.OrderProduct", related_name="orders"
    )
    order_date = models.DateTimeField(auto_now_add=True)
    payment_due_date = models.DateTimeField()

    def __str__(self):
        return f"{self.user.user.username} {self.order_date}"


class OrderProduct(models.Model):
    product = models.ForeignKey(Product, on_delete=models.CASCADE)
    order = models.ForeignKey(Order, on_delete=models.CASCADE)
    quantity = models.PositiveIntegerField()

    def __str__(self):
        return f"{self.order.user.user.username} {self.order.order_date}"


class UserProfile(models.Model):
    class RoleChoice(models.TextChoices):
        CLIENT = "Client", "Client"
        SELLER = "Seller", "Seller"

    user = models.OneToOneField(
        User, related_name="user_details", null=False, on_delete=models.CASCADE
    )
    role = models.CharField(
        max_length=30, choices=RoleChoice.choices, default=RoleChoice.CLIENT
    )

    def __str__(self):
        return f"{self.user.username} ({self.role})"
