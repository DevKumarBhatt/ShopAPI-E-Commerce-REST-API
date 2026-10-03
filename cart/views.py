# from django.shortcuts import render

# # Create your views here.
from rest_framework import status
from rest_framework.permissions import IsAuthenticated
from rest_framework.response import Response
from rest_framework.views import APIView

from drf_spectacular.utils import extend_schema

from products.models import Product

from .models import Cart, CartItem
from .serializers import CartSerializer, CartItemSerializer


class CartView(APIView):
    permission_classes = [IsAuthenticated]

    def get_cart(self, user):
        cart, created = Cart.objects.get_or_create(user=user)
        return cart

    @extend_schema(
        responses=CartSerializer
    )
    def get(self, request):
        cart = self.get_cart(request.user)

        serializer = CartSerializer(cart)

        return Response(serializer.data)

    @extend_schema(
        request=CartItemSerializer,
        responses={201: CartSerializer}
    )
    def post(self, request):
        cart = self.get_cart(request.user)

        serializer = CartItemSerializer(data=request.data)

        if not serializer.is_valid():
            return Response(
                serializer.errors,
                status=status.HTTP_400_BAD_REQUEST
            )

        product = serializer.validated_data["product"]
        quantity = serializer.validated_data["quantity"]

        if not product.is_active:
            return Response(
                {"error": "Product is not active."},
                status=status.HTTP_400_BAD_REQUEST
            )

        if quantity > product.stock:
            return Response(
                {"error": "Requested quantity is not available in stock."},
                status=status.HTTP_400_BAD_REQUEST
            )

        cart_item, created = CartItem.objects.get_or_create(
            cart=cart,
            product=product,
            defaults={"quantity": quantity}
        )

        if not created:
            new_quantity = cart_item.quantity + quantity

            if new_quantity > product.stock:
                return Response(
                    {"error": "Requested quantity exceeds available stock."},
                    status=status.HTTP_400_BAD_REQUEST
                )

            cart_item.quantity = new_quantity
            cart_item.save()

        cart_serializer = CartSerializer(cart)

        return Response(
            cart_serializer.data,
            status=status.HTTP_201_CREATED
        )


class CartItemView(APIView):
    permission_classes = [IsAuthenticated]

    def get_item(self, request, item_id):
        try:
            return CartItem.objects.get(
                id=item_id,
                cart__user=request.user
            )
        except CartItem.DoesNotExist:
            return None

    @extend_schema(
        request=CartItemSerializer,
        responses={200: CartSerializer}
    )
    def patch(self, request, item_id):
        cart_item = self.get_item(request, item_id)

        if not cart_item:
            return Response(
                {"error": "Cart item not found."},
                status=status.HTTP_404_NOT_FOUND
            )

        quantity = request.data.get("quantity")

        if quantity is None:
            return Response(
                {"error": "Quantity is required."},
                status=status.HTTP_400_BAD_REQUEST
            )

        try:
            quantity = int(quantity)
        except (TypeError, ValueError):
            return Response(
                {"error": "Quantity must be a valid number."},
                status=status.HTTP_400_BAD_REQUEST
            )

        if quantity < 1:
            return Response(
                {"error": "Quantity must be at least 1."},
                status=status.HTTP_400_BAD_REQUEST
            )

        if quantity > cart_item.product.stock:
            return Response(
                {"error": "Requested quantity is not available in stock."},
                status=status.HTTP_400_BAD_REQUEST
            )

        cart_item.quantity = quantity
        cart_item.save()

        cart = cart_item.cart
        serializer = CartSerializer(cart)

        return Response(serializer.data)

    @extend_schema(
        responses={200: CartSerializer}
    )
    def delete(self, request, item_id):
        cart_item = self.get_item(request, item_id)

        if not cart_item:
            return Response(
                {"error": "Cart item not found."},
                status=status.HTTP_404_NOT_FOUND
            )

        cart = cart_item.cart
        cart_item.delete()

        serializer = CartSerializer(cart)

        return Response(serializer.data)