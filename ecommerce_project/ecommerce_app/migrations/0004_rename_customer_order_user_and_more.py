# Generated by Django 4.0.3 on 2023-10-25 19:18

from django.db import migrations


class Migration(migrations.Migration):

    dependencies = [
        ('ecommerce_app', '0003_alter_order_products_and_more'),
    ]

    operations = [
        migrations.RenameField(
            model_name='order',
            old_name='customer',
            new_name='user',
        ),
        migrations.AlterUniqueTogether(
            name='orderproduct',
            unique_together=set(),
        ),
    ]
