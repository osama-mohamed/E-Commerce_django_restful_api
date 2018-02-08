from django.conf.urls import url
from .views import (
    AddToCartAPIView,
    CartAPIView,
    OrderUpdateAPIView,
    PendingOrdersAPIView,
    AcceptedOrdersAPIView,
    RejectedOrdersAPIView,
)

urlpatterns = [
    url(r'^order/(?P<id>\d+)/$', AddToCartAPIView.as_view(), name='order_api'),
    url(r'^order/(?P<id>\d+)/update/$', OrderUpdateAPIView.as_view(), name='update_api'),
    # url(r'^order/(?P<id>\d+)/delete/$', OrderDeleteView.as_view(), name='delete'),
    url(r'^cart/$', CartAPIView.as_view(), name='cart_api'),
    url(r'^pending/$', PendingOrdersAPIView.as_view(), name='pending_api'),
    url(r'^rejected/$', RejectedOrdersAPIView.as_view(), name='rejected_api'),
    url(r'^accepted/$', AcceptedOrdersAPIView.as_view(), name='accepted_api'),
    # url(r'^thank_you/$', BuyThankView.as_view(), name='thank'),
    # url(r'^buy/$', BuyOrdersView.as_view(), name='buy'),
]
