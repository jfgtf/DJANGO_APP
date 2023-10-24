from django.db import models
from django.contrib.auth.models import User


class Category(models.Model):
    name = models.CharField(max_length=100)


class Product(models.Model):
    name = models.CharField(max_length=100)
    description = models.TextField()
    price = models.DecimalField(max_digits=10, decimal_places=2)
    category = models.ForeignKey(Category, on_delete=models.CASCADE)
    image = models.ImageField(upload_to='assets/images/')
    thumbnail = models.ImageField(upload_to='assets/thumbnails/')


class Order(models.Model):
    customer = models.ForeignKey(User, on_delete=models.CASCADE)
    shipping_address = models.TextField()
    products = models.ManyToManyField(Product, through='OrderProduct')
    order_date = models.DateTimeField(auto_now_add=True)
    payment_due_date = models.DateTimeField()


class OrderProduct(models.Model):
    product = models.ForeignKey(Product, on_delete=models.CASCADE)
    order = models.ForeignKey(Order, on_delete=models.CASCADE)
    quantity = models.PositiveIntegerField()


class UserProfile(models.Model):
    user = models.OneToOneField(User, on_delete=models.CASCADE)
    is_seller = models.BooleanField(default=False)
