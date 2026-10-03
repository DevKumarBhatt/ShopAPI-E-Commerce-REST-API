from rest_framework import serializers

from .models import Cart, CartItem


class CartItemSerializer(serializers.ModelSerializer):
    product_name = serializers.CharField(
        source="product.name",
        read_only=True
    )

    product_price = serializers.DecimalField(
        source="product.price",
        max_digits=10,
        decimal_places=2,
        read_only=True
    )

    subtotal = serializers.SerializerMethodField()

    class Meta:
        model = CartItem
        fields = [
            "id",
            "product",
            "product_name",
            "product_price",
            "quantity",
            "subtotal",
        ]
        read_only_fields = [
            "id",
            "product_name",
            "product_price",
            "subtotal",
        ]

    def get_subtotal(self, obj):
        return obj.product.price * obj.quantity


class CartSerializer(serializers.ModelSerializer):
    items = CartItemSerializer(
        many=True,
        read_only=True
    )

    total_price = serializers.SerializerMethodField()

    class Meta:
        model = Cart
        fields = [
            "id",
            "items",
            "total_price",
            "created_at",
            "updated_at",
        ]
        read_only_fields = [
            "id",
            "items",
            "total_price",
            "created_at",
            "updated_at",
        ]

    def get_total_price(self, obj):
        return sum(
            item.product.price * item.quantity
            for item in obj.items.all()
        )