from decimal import Decimal

from django.db import transaction
from drf_spectacular.utils import extend_schema
from rest_framework import status
from rest_framework.permissions import IsAuthenticated
from rest_framework.response import Response
from rest_framework.views import APIView

from cart.models import Cart

from .models import Order, OrderItem
from .serializers import ErrorSerializer, OrderSerializer


class OrderListCreateView(APIView):
    permission_classes = [IsAuthenticated]

    @extend_schema(
        responses={
            200: OrderSerializer(many=True),
        }
    )
    def get(self, request):
        orders = Order.objects.filter(
            user=request.user
        ).prefetch_related("items__product")

        serializer = OrderSerializer(
            orders,
            many=True
        )

        return Response(serializer.data)

    @transaction.atomic
    @extend_schema(
        responses={
            201: OrderSerializer,
            400: ErrorSerializer,
        }
    )
    def post(self, request):
        try:
            cart = Cart.objects.get(
                user=request.user
            )
        except Cart.DoesNotExist:
            return Response(
                {"error": "Cart is empty."},
                status=status.HTTP_400_BAD_REQUEST
            )

        cart_items = cart.items.select_related("product")

        if not cart_items.exists():
            return Response(
                {"error": "Cart is empty."},
                status=status.HTTP_400_BAD_REQUEST
            )

        total_amount = Decimal("0.00")

        for cart_item in cart_items:
            product = cart_item.product

            if not product.is_active:
                return Response(
                    {
                        "error": (
                            f"{product.name} is not available."
                        )
                    },
                    status=status.HTTP_400_BAD_REQUEST
                )

            if cart_item.quantity > product.stock:
                return Response(
                    {
                        "error": (
                            f"Insufficient stock for "
                            f"{product.name}."
                        )
                    },
                    status=status.HTTP_400_BAD_REQUEST
                )

            total_amount += (
                product.price * cart_item.quantity
            )

        order = Order.objects.create(
            user=request.user,
            total_amount=total_amount
        )

        for cart_item in cart_items:
            product = cart_item.product

            OrderItem.objects.create(
                order=order,
                product=product,
                quantity=cart_item.quantity,
                price=product.price,
                subtotal=(
                    product.price * cart_item.quantity
                )
            )

            product.stock -= cart_item.quantity

            product.save(
                update_fields=["stock"]
            )

        cart.items.all().delete()

        serializer = OrderSerializer(order)

        return Response(
            serializer.data,
            status=status.HTTP_201_CREATED
        )


class OrderDetailView(APIView):
    permission_classes = [IsAuthenticated]

    @extend_schema(
        responses={
            200: OrderSerializer,
            404: ErrorSerializer,
        }
    )
    def get(self, request, order_id):
        try:
            order = Order.objects.prefetch_related(
                "items__product"
            ).get(
                id=order_id,
                user=request.user
            )
        except Order.DoesNotExist:
            return Response(
                {"error": "Order not found."},
                status=status.HTTP_404_NOT_FOUND
            )

        serializer = OrderSerializer(order)

        return Response(serializer.data)