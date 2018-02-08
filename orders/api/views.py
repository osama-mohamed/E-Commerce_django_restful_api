from rest_framework.generics import (
    CreateAPIView,
    RetrieveAPIView,
    RetrieveUpdateAPIView,
    UpdateAPIView,
    DestroyAPIView,
    ListAPIView,
)

from rest_framework.response import Response
from rest_framework.status import HTTP_200_OK, HTTP_400_BAD_REQUEST
from rest_framework.views import APIView
from rest_framework.permissions import IsAuthenticatedOrReadOnly, IsAdminUser, IsAuthenticated, AllowAny

# from django.contrib.auth import get_user_model, update_session_auth_hash

from .serializers import (
    OrdersSerializer,
    CartSerializer,
    OrderUpdateSerializer,
)
from accounts.models import Account
from products.models import Product
from orders.models import Checkout
from .permissions import IsOwnerOrReadOnly

# User = get_user_model()


class AddToCartAPIView(APIView):
    permission_classes = [IsAuthenticatedOrReadOnly, IsAuthenticated]

    def post(self, request, id):
        user = self.request.user
        if user.is_authenticated():
            qs = Checkout.objects.filter(product_id=id, status='waiting')
            if qs.exists():
                return Response({'message': ['already exists!']}, status=HTTP_200_OK)
            else:
                product = Product.objects.filter(id=id, publish=True).first()
                checkout = Checkout.objects.create(
                    user=self.request.user,
                    product_id=id,
                    name=product.name,
                    slug=product.slug,
                    price=product.price,
                    quantity=1,
                    discount=product.discount,
                    image=product.image,
                )
                return Response({'message': ['added successfully!']}, status=HTTP_200_OK)
        else:
            return Response({'message': ['you must be logged in first!']}, status=HTTP_200_OK)


class CartAPIView(ListAPIView):
    serializer_class = CartSerializer
    # queryset = Product.objects.all().order_by('-id')
    permission_classes = [IsAuthenticatedOrReadOnly, IsAuthenticated]

    def get_queryset(self, *args, **kwargs):
        queryset = Checkout.objects.filter(user=self.request.user, status='waiting').order_by('-id')
        return queryset


class PendingOrdersAPIView(ListAPIView):
    serializer_class = OrdersSerializer
    # queryset = Product.objects.all().order_by('-id')
    permission_classes = [IsAuthenticatedOrReadOnly, IsAuthenticated]

    def get_queryset(self, *args, **kwargs):
        queryset = Checkout.objects.filter(user=self.request.user, status='pending').order_by('-id')
        return queryset


class AcceptedOrdersAPIView(ListAPIView):
    serializer_class = OrdersSerializer
    # queryset = Product.objects.all().order_by('-id')
    permission_classes = [IsAuthenticatedOrReadOnly, IsAuthenticated]

    def get_queryset(self, *args, **kwargs):
        queryset = Checkout.objects.filter(user=self.request.user, status='accepted').order_by('-id')
        return queryset


class RejectedOrdersAPIView(ListAPIView):
    serializer_class = OrdersSerializer
    # queryset = Product.objects.all().order_by('-id')
    permission_classes = [IsAuthenticatedOrReadOnly, IsAuthenticated]

    def get_queryset(self, *args, **kwargs):
        queryset = Checkout.objects.filter(user=self.request.user, status='rejected').order_by('-id')
        return queryset


class OrderUpdateAPIView(RetrieveUpdateAPIView):
    serializer_class = OrderUpdateSerializer
    # queryset = Checkout.objects.all()
    lookup_field = 'id'
    lookup_url_kwarg = 'id'
    permission_classes = [IsOwnerOrReadOnly, IsAuthenticated]

    def get_queryset(self, *args, **kwargs):
        queryset = Checkout.objects.filter(user=self.request.user, status='waiting').order_by('-id')
        return queryset

