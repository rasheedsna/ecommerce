# Generated by Django 4.0.4 on 2022-06-03 10:52

from django.conf import settings
from django.db import migrations, models
import django.db.models.deletion
import uuid


class Migration(migrations.Migration):

    dependencies = [
        migrations.swappable_dependency(settings.AUTH_USER_MODEL),
        ('orders', '0002_alter_cart_options_alter_cart_cart_owner'),
    ]

    operations = [
        migrations.RemoveField(
            model_name='cart',
            name='cart_owner',
        ),
        migrations.CreateModel(
            name='Order',
            fields=[
                ('_id', models.UUIDField(default=uuid.uuid4, editable=False, primary_key=True, serialize=False)),
                ('name', models.CharField(max_length=100)),
                ('address', models.CharField(max_length=250)),
                ('contact', models.CharField(max_length=20)),
                ('paymentMethod', models.CharField(max_length=50)),
                ('status', models.CharField(choices=[('Delivered', 'Delivered'), ('Pending', 'Pending'), ('Processing', 'Processing'), ('Cancel', 'Cancel')], default='Pending', max_length=10)),
                ('subTotal', models.DecimalField(decimal_places=2, max_digits=10)),
                ('shippingCost', models.DecimalField(decimal_places=2, max_digits=10)),
                ('total', models.DecimalField(decimal_places=2, max_digits=10)),
                ('invoice', models.CharField(max_length=20)),
                ('createdAt', models.DateTimeField(auto_now_add=True)),
                ('updatedAt', models.DateTimeField(auto_now=True)),
                ('user', models.ForeignKey(on_delete=django.db.models.deletion.CASCADE, to=settings.AUTH_USER_MODEL)),
            ],
        ),
    ]