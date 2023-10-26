from background_task import background
from django.conf import settings
from django.core.mail import send_mail
from django.utils import timezone
from ecommerce_app.models import Order


@background(schedule=timezone.timedelta(days=settings.DAYS_UNTIL_PAYMENT - 1))
def send_schedule_email(order_id):
    order = Order.objects.get(id=order_id)
    user = order.user_details.user

    send_mail(
        "Order payment reminder",
        (
            "We kindly remind You to pay for your order."
            "Disregard this mail if You have already paid "
            f"Your payment is due by {order.payment_due_date}."
        ),
        settings.EMAIL,
        [user.email],
        fail_silently=False,
    )
