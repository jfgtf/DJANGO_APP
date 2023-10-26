from datetime import datetime

from django.conf import settings
from django.core.mail import send_mail
from django.db.models import Sum
from django.utils import timezone
from ecommerce_app.mail_auto_send import send_schedule_email
from ecommerce_app.models import (
    Category,
    Order,
    OrderProduct,
    Product,
    UserProfile,
)
from ecommerce_app.permissions import (
    CanEditProduct,
    CanPlaceOrder,
    IsUserSeller,
)
from ecommerce_app.serializers import (
    CategorySerializer,
    OrderSerializer,
    ProductSerializer,
    UserProfileSerializer,
)
from rest_framework import filters, generics, mixins, viewsets
from rest_framework.pagination import LimitOffsetPagination
from rest_framework.response import Response
from rest_framework.views import APIView


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


class OrderViewset(
    mixins.CreateModelMixin,
    mixins.ListModelMixin,
    mixins.RetrieveModelMixin,
    viewsets.GenericViewSet,
):
    queryset = Order.objects.all()
    serializer_class = OrderSerializer
    permission_classes = [CanPlaceOrder]

    def create(self, request):
        data = request.POST.copy()

        payment_due_date = timezone.now() + timezone.timedelta(
            days=settings.DAYS_UNTIL_PAYMENT
        )
        data["payment_due_date"] = payment_due_date

        serializer = self.get_serializer(data=data)
        serializer.is_valid(raise_exception=True)
        serializer.save()
        order = serializer.instance
        send_schedule_email(order.id)
        user = order.user_details.user

        send_mail(
            "Order Confirmation",
            (
                "Thank you for your order."
                f" Your payment is due by {payment_due_date}."
            ),
            settings.EMAIL,
            [user.email],
            fail_silently=False,
        )

        headers = self.get_success_headers(serializer.data)
        return Response(serializer.data, status=201, headers=headers)


class TopOrderedProducts(APIView):
    permission_classes = [IsUserSeller]

    def get(self, request):
        data = request.data

        date_format = "%Y-%m-%dT%H:%M:%S.%fZ"

        start_date = datetime.strptime(data.get("date_from"), date_format)
        end_date = datetime.strptime(data.get("date_to"), date_format)
        num_products = int(data.get("product_number"))

        top_products = (
            OrderProduct.objects.filter(
                order__order_date__range=[start_date, end_date]
            )
            .values("product__name")
            .annotate(total_ordered=Sum("quantity"))
            .order_by("-total_ordered")[:num_products]
        )

        return Response(top_products, status=200)
