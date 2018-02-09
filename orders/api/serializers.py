from rest_framework.serializers import (
    ModelSerializer,
    ValidationError,
    HyperlinkedIdentityField,
    SerializerMethodField,
)

from django.core.urlresolvers import reverse
from django.conf import settings

from orders.models import Checkout
from products.models import Product


class OrdersSerializer(ModelSerializer):
    user = SerializerMethodField(read_only=True)

    class Meta:
        model = Checkout
        fields = [
            'id',
            'user',
            'status',
            'product_id',
            'name',
            'price',
            'discount',
            'quantity',
            'image',
            'slug',
            'added',
            'updated',
        ]

    def get_user(self, obj):
        return str(obj.user)


class CartSerializer(ModelSerializer):
    user = SerializerMethodField(read_only=True)
    edit_url = HyperlinkedIdentityField(
        view_name='orders_api:update_api',
        lookup_field='id',
    )
    delete_url = HyperlinkedIdentityField(
        view_name='orders_api:delete_api',
        lookup_field='id',
    )

    class Meta:
        model = Checkout
        fields = [
            'id',
            'edit_url',
            'delete_url',
            'user',
            'status',
            'product_id',
            'name',
            'price',
            'discount',
            'quantity',
            'image',
            'slug',
            'added',
            'updated',
        ]

    def get_user(self, obj):
        return str(obj.user)


class OrderUpdateSerializer(ModelSerializer):
    user = SerializerMethodField(read_only=True)
    all_orders_url = SerializerMethodField()

    class Meta:
        model = Checkout
        fields = [
            'id',
            'all_orders_url',
            'user',
            'status',
            'product_id',
            'name',
            'price',
            'discount',
            'quantity',
            'image',
            'slug',
            'added',
            'updated',
        ]
        read_only_fields = [
            'id',
            'user',
            'status',
            'name',
            'price',
            'discount',
            'image',
            'slug',
        ]

    def get_user(self, obj):
        return str(obj.user)

    def get_all_orders_url(self, obj):
        return str(settings.BASE_URL + reverse('orders_api:cart_api'))

    def validate(self, data):
        product_id = data.get('product_id')
        quantity = data.get('quantity')
        available = Product.objects.filter(id=product_id).first().quantity
        if quantity > available:
            raise ValidationError('Quantity more than the available quantity = {}!'.format(available))
        if quantity == 0:
            raise ValidationError('Quantity can not be less than 1')
        return data
