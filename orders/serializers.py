from rest_framework import serializers

from .models import Order, OrderItem


class OrderItemSerializer(serializers.ModelSerializer):
    product_name = serializers.CharField(
        source="product.name",
        read_only=True
    )

    class Meta:
        model = OrderItem
        fields = [
            "id",
            "product",
            "product_name",
            "quantity",
            "price",
            "subtotal",
        ]
        read_only_fields = [
            "id",
            "product_name",
            "price",
            "subtotal",
        ]


class OrderSerializer(serializers.ModelSerializer):
    items = OrderItemSerializer(
        many=True,
        read_only=True
    )

    class Meta:
        model = Order
        fields = [
            "id",
            "user",
            "items",
            "total_amount",
            "status",
            "created_at",
            "updated_at",
        ]
        read_only_fields = [
            "id",
            "user",
            "items",
            "total_amount",
            "status",
            "created_at",
            "updated_at",
        ]
        
class ErrorSerializer(serializers.Serializer):
    error = serializers.CharField()        