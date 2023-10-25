from django.core.mail import send_mail
from django.db.models import Count
from django.utils import timezone
from ecommerce_app.models import (
    Category,
    Order,
    OrderProduct,
    Product,
    UserProfile,
)
from ecommerce_app.permissions import CanEditProduct
from ecommerce_app.serializers import (
    CategorySerializer,
    OrderProductSerializer,
    OrderSerializer,
    ProductSerializer,
    UserProfileSerializer,
)
from rest_framework import filters, generics, mixins, permissions, viewsets
from rest_framework.pagination import LimitOffsetPagination
from rest_framework.response import Response


class CategoryViewset(
    mixins.CreateModelMixin,
    mixins.ListModelMixin,
    mixins.RetrieveModelMixin,
    viewsets.GenericViewSet,
):
    queryset = Category.objects.all()
    serializer_class = CategorySerializer


class ProductViewset(
    mixins.CreateModelMixin,
    mixins.ListModelMixin,
    mixins.RetrieveModelMixin,
    viewsets.GenericViewSet,
):
    queryset = Product.objects.all()
    serializer_class = ProductSerializer
    filter_backends = [filters.SearchFilter, filters.OrderingFilter]
    pagination_class = LimitOffsetPagination
    search_fields = ["name", "category__name", "description"]
    ordering_fields = ["name", "category__name", "price"]
    permission_classes = [CanEditProduct]


class UserList(generics.ListCreateAPIView):
    queryset = UserProfile.objects.all()
    serializer_class = UserProfileSerializer


class OrderList(generics.ListCreateAPIView):
    queryset = Order.objects.all()
    serializer_class = OrderSerializer


class OrderDetail(generics.RetrieveUpdateDestroyAPIView):
    queryset = Order.objects.all()
    serializer_class = OrderSerializer


class OrderPlacement(generics.CreateAPIView):
    serializer_class = OrderSerializer
    permission_classes = [permissions.IsAuthenticated]

    def create(self, request, *args, **kwargs):
        if request.method == "POST":
            data = request.POST.copy()

            customer_name = data.get("customer_name")
            # shipping_address = data.get("shipping_address")
            # products = data.get("products")

            payment_due_date = timezone.now() + timezone.timedelta(days=5)
            data["payment_due_date"] = payment_due_date

            serializer = self.get_serializer(data=data)
            serializer.is_valid(raise_exception=True)
            serializer.save()

            subject = "Order Confirmation"
            message = (
                "Thank you for your order."
                f" Your payment is due by {payment_due_date}."
            )
            from_email = "your@email.com"
            recipient_list = [customer_name]

            send_mail(
                subject,
                message,
                from_email,
                recipient_list,
                fail_silently=False,
            )

            headers = self.get_success_headers(serializer.data)
            return Response(serializer.data, status=201, headers=headers)


class TopOrderedProducts(generics.ListAPIView):
    permission_classes = [permissions.IsAuthenticated]

    def list(self, request, *args, **kwargs):
        data = request.data

        start_date = data.get("date_from")
        end_date = data.get("date_to")
        num_products = data.get("product_number")

        top_products = (
            OrderProduct.objects.filter(
                order__order_date__range=[start_date, end_date]
            )
            .values("product__name")
            .annotate(total_ordered=Count("product"))
            .order_by("-total_ordered")[:num_products]
        )

        serializer = OrderProductSerializer(top_products, many=True)

        return Response(serializer.data)
