# Generated by Django 4.0.3 on 2023-10-25 18:43

from django.db import migrations, models


class Migration(migrations.Migration):

    dependencies = [
        ('ecommerce_app', '0002_remove_userprofile_is_seller_userprofile_role'),
    ]

    operations = [
        migrations.AlterField(
            model_name='order',
            name='products',
            field=models.ManyToManyField(related_name='orders', through='ecommerce_app.OrderProduct', to='ecommerce_app.product'),
        ),
        migrations.AlterUniqueTogether(
            name='orderproduct',
            unique_together={('order', 'product')},
        ),
    ]
