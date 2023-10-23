from rest_framework import serializers
from .models import Product, Order, Category, OrderProduct, UserProfile


class CategorySerializer(serializers.ModelSerializer):
    class Meta:
        model = Category
        fields = '__all__'


class ProductSerializer(serializers.ModelSerializer):
    category = CategorySerializer()

    class Meta:
        model = Product
        fields = '__all__'


class OrderProductSerializer(serializers.ModelSerializer):
    class Meta:
        model = OrderProduct
        fields = '__all__'


class OrderSerializer(serializers.ModelSerializer):
    customer = serializers.StringRelatedField()
    products = OrderProductSerializer(many=True, read_only=True)

    class Meta:
        model = Order
        fields = '__all__'


class UserProfileSerializer(serializers.ModelSerializer):
    user = serializers.StringRelatedField()

    class Meta:
        model = UserProfile
        fields = '__all__'
