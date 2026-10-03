from django.urls import path

from .views import OrderListCreateView, OrderDetailView


urlpatterns = [
    path(
        "",
        OrderListCreateView.as_view(),
        name="orders"
    ),
    path(
        "<int:order_id>/",
        OrderDetailView.as_view(),
        name="order-detail"
    ),
]