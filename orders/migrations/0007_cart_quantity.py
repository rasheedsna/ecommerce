# Generated by Django 4.0.4 on 2022-06-04 09:41

from django.db import migrations, models


class Migration(migrations.Migration):

    dependencies = [
        ('orders', '0006_cart_discount_cart_itemtotal_alter_cart_order'),
    ]

    operations = [
        migrations.AddField(
            model_name='cart',
            name='quantity',
            field=models.PositiveIntegerField(default=1, max_length=4),
        ),
    ]
