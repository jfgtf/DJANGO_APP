from rest_framework import serializers

from .models import Category, Order, OrderProduct, Product, UserProfile


class CategorySerializer(serializers.ModelSerializer):
    class Meta:
        model = Category
        fields = "__all__"


class ProductSerializer(serializers.ModelSerializer):
    category = serializers.PrimaryKeyRelatedField(
        queryset=Category.objects.all(), write_only=True
    )

    class Meta:
        model = Product
        fields = "__all__"


class OrderProductSerializer(serializers.ModelSerializer):
    class Meta:
        model = OrderProduct
        fields = "__all__"


class OrderSerializer(serializers.ModelSerializer):
    user = serializers.PrimaryKeyRelatedField(
        queryset=UserProfile.objects.all(), write_only=True
    )
    products = OrderProductSerializer(many=True, read_only=True)

    class Meta:
        model = Order
        fields = "__all__"


class UserProfileSerializer(serializers.ModelSerializer):
    user = serializers.StringRelatedField()

    class Meta:
        model = UserProfile
        fields = "__all__"
