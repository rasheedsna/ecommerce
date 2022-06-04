from rest_framework import serializers
from . models import Order, Cart
from  shop.serializers import ProductSerializer


class CartSerializer(serializers.ModelSerializer):

    class Meta:
        model = Cart
        fields = ['id', 'createdAt', 'updatedAt', 'discount', 'itemTotal', 'product']

    def to_representation(self, instance):
        response = super().to_representation(instance)
        response['product'] = ProductSerializer(instance.product).data
        return response


class OrderSerializer(serializers.ModelSerializer):
    queryset = Cart.objects.all()
    cart = CartSerializer(queryset, many=True)

    class Meta:
        model = Order
        fields = ['_id', 'cart', 'name', 'address', 'contact', 'paymentMethod', 'status', 'subTotal', 'shippingCost',
                  'total', 'invoice', 'createdAt', 'updatedAt', 'user']

    def create(self, validated_data):
        name = validated_data.get('name')
        address = validated_data.get('address')
        contact = validated_data.get('contact')
        payment_method = validated_data.get('paymentMethod')
        status = validated_data.get('status')
        sub_total = validated_data.get('subTotal')
        shipping_cost = validated_data.get('shippingCost')
        total = validated_data.get('total')
        invoice = validated_data.get('invoice')
        user = validated_data.get('user')

        order = Order.objects.create(
            name=name,
            address=address,
            contact=contact,
            paymentMethod=payment_method,
            status=status,
            subTotal=sub_total,
            shippingCost=shipping_cost,
            total=total,
            invoice=invoice,
            user=user
        )
        order.save()

        cart_items = validated_data.get('cart')
        for cart_item in cart_items:
            cart = Cart.objects.create(
                order=order,
                **cart_item
            )
            cart.save()

        return order

    def update(self, instance, validated_data):
        instance.status = validated_data('status', instance.status)
        instance.save()

        return instance

