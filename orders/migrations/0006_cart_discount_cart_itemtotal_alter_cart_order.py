# Generated by Django 4.0.4 on 2022-06-04 05:33

from django.db import migrations, models
import django.db.models.deletion


class Migration(migrations.Migration):

    dependencies = [
        ('orders', '0005_alter_cart_order'),
    ]

    operations = [
        migrations.AddField(
            model_name='cart',
            name='discount',
            field=models.DecimalField(decimal_places=2, default=0, max_digits=10),
        ),
        migrations.AddField(
            model_name='cart',
            name='itemTotal',
            field=models.DecimalField(decimal_places=2, default=0, max_digits=10),
        ),
        migrations.AlterField(
            model_name='cart',
            name='order',
            field=models.ForeignKey(on_delete=django.db.models.deletion.CASCADE, related_name='cart', to='orders.order'),
        ),
    ]
