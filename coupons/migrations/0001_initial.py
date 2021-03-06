# Generated by Django 4.0.4 on 2022-06-04 11:47

from django.db import migrations, models
import django.db.models.deletion
import uuid


class Migration(migrations.Migration):

    initial = True

    dependencies = [
        ('shop', '0002_remove_tag_product_tag_product'),
    ]

    operations = [
        migrations.CreateModel(
            name='Coupons',
            fields=[
                ('_id', models.UUIDField(default=uuid.uuid4, editable=False, primary_key=True, serialize=False)),
                ('createdAt', models.DateTimeField(auto_now_add=True)),
                ('updatedAt', models.DateTimeField(auto_now=True)),
                ('discountPercentage', models.DecimalField(decimal_places=2, default=0, max_digits=2)),
                ('title', models.CharField(max_length=100)),
                ('couponCode', models.CharField(max_length=10)),
                ('endTime', models.DateTimeField()),
                ('minimumAmount', models.DecimalField(decimal_places=2, default=0, max_digits=10)),
                ('logo', models.ImageField(upload_to='coupon_banner')),
                ('productType', models.ForeignKey(on_delete=django.db.models.deletion.CASCADE, to='shop.type')),
            ],
            options={
                'verbose_name': 'Coupon',
                'verbose_name_plural': 'Coupons',
                'ordering': ('-updatedAt',),
            },
        ),
    ]
