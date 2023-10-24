from rest_framework import generics
from rest_framework import permissions
from rest_framework import filters
from rest_framework.response import Response

from django.utils import timezone
from django.core.mail import send_mail
from django.db.models import Count

from .models import Product, Order, OrderProduct
from .serializers import ProductSerializer, OrderSerializer, OrderProductSerializer


class ProductList(generics.ListCreateAPIView):
    queryset = Product.objects.all()
    serializer_class = ProductSerializer
    filter_backends = [filters.SearchFilter, filters.OrderingFilter]
    search_fields = ['name', 'category__name', 'description']
    ordering_fields = ['name', 'category__name', 'price']


class ProductDetail(generics.RetrieveUpdateDestroyAPIView):
    queryset = Product.objects.all()
    serializer_class = ProductSerializer


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
        data = request.data

        # Process the order data
        customer_name = data.get('customer_name')
        shipping_address = data.get('shipping_address')
        products = data.get('products')  # Assuming it's a list of product IDs and quantities

        # Calculate the payment date
        payment_due_date = timezone.now() + timezone.timedelta(days=5)
        data['payment_due_date'] = payment_due_date

        # Create the order
        serializer = self.get_serializer(data=data)
        serializer.is_valid(raise_exception=True)
        serializer.save()

        # Send an email confirmation to the customer 
        subject = 'Order Confirmation'
        message = f'Thank you for your order. Your payment is due by {payment_due_date}.'
        from_email = 'your@email.com'
        recipient_list = [customer_name] 

        send_mail(subject, message, from_email, recipient_list, fail_silently=False)

        headers = self.get_success_headers(serializer.data)
        return Response(serializer.data, status=201, headers=headers)


class TopOrderedProducts(generics.ListAPIView):
    permission_classes = [permissions.IsAuthenticated]

    def list(self, request, *args, **kwargs):
        data = request.data

        # Process input parameters, e.g., data_od (start date), data_do (end date), and liczba_produktów (number of products)
        start_date = data.get('data_od')  # Replace with your parameter name
        end_date = data.get('data_do')  # Replace with your parameter name
        num_products = data.get('liczba_produktów')  # Replace with your parameter name

        # Query for the top ordered products
        top_products = OrderProduct.objects.filter(
            order__order_date__range=[start_date, end_date]
        ).values('product__name').annotate(total_ordered=Count('product')).order_by('-total_ordered')[:num_products]

        # Serialize the results
        serializer = OrderProductSerializer(top_products, many=True)

        return Response(serializer.data)
