from io import BytesIO

from django.core.files.uploadedfile import SimpleUploadedFile
from django.db.models.signals import pre_save
from django.dispatch import receiver
from ecommerce_app.models import Product
from PIL import Image


@receiver(pre_save, sender=Product)
def generate_thumbnail(sender, instance, **kwargs):
    if instance.image and (
        not instance.pk
        or instance.image != Product.objects.get(pk=instance.pk).image
    ):
        image = Image.open(instance.image)
        image_name = image.fp.name.rsplit(".", 1)[0]

        thumbnail = image.copy()
        thumbnail.thumbnail((200, 200))

        thumbnail_buffer = BytesIO()
        thumbnail.save(thumbnail_buffer, "JPEG")

        thumbnail_file = SimpleUploadedFile(
            name=f"{image_name}-thumbnail.jpg",
            content=thumbnail_buffer.getvalue(),
            content_type="image/jpeg",
        )

        instance.thumbnail = thumbnail_file
