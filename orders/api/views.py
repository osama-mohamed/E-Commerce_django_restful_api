from rest_framework.generics import (
    RetrieveUpdateAPIView,
    DestroyAPIView,
    ListAPIView,
)

from rest_framework.response import Response
from rest_framework.status import HTTP_200_OK, HTTP_400_BAD_REQUEST
from rest_framework.views import APIView
from rest_framework.permissions import IsAuthenticatedOrReadOnly, IsAuthenticated

from .serializers import (
    OrdersSerializer,
    CartSerializer,
    OrderUpdateSerializer,
)
from accounts.models import Account
from products.models import Product
from orders.models import Checkout
from .permissions import IsOwnerOrReadOnly


class AddToCartAPIView(APIView):
    permission_classes = [IsAuthenticatedOrReadOnly, IsAuthenticated]

    def post(self, request, id):
        user = self.request.user
        if user.is_authenticated():
            qs = Checkout.objects.filter(product_id=id, user=user, status='waiting')
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
    permission_classes = [IsAuthenticatedOrReadOnly, IsAuthenticated]

    def get_queryset(self, *args, **kwargs):
        queryset = Checkout.objects.filter(user=self.request.user, status='waiting').order_by('-id')
        return queryset


class PendingOrdersAPIView(ListAPIView):
    serializer_class = OrdersSerializer
    permission_classes = [IsAuthenticatedOrReadOnly, IsAuthenticated]

    def get_queryset(self, *args, **kwargs):
        queryset = Checkout.objects.filter(user=self.request.user, status='pending').order_by('-id')
        return queryset


class AcceptedOrdersAPIView(ListAPIView):
    serializer_class = OrdersSerializer
    permission_classes = [IsAuthenticatedOrReadOnly, IsAuthenticated]

    def get_queryset(self, *args, **kwargs):
        queryset = Checkout.objects.filter(user=self.request.user, status='accepted').order_by('-id')
        return queryset


class RejectedOrdersAPIView(ListAPIView):
    serializer_class = OrdersSerializer
    permission_classes = [IsAuthenticatedOrReadOnly, IsAuthenticated]

    def get_queryset(self, *args, **kwargs):
        queryset = Checkout.objects.filter(user=self.request.user, status='rejected').order_by('-id')
        return queryset


class OrderUpdateAPIView(RetrieveUpdateAPIView):
    serializer_class = OrderUpdateSerializer
    lookup_field = 'id'
    lookup_url_kwarg = 'id'
    permission_classes = [IsOwnerOrReadOnly, IsAuthenticated]

    def get_queryset(self, *args, **kwargs):
        queryset = Checkout.objects.filter(user=self.request.user, status='waiting').order_by('-id')
        return queryset


class OrderDeleteAPIView(DestroyAPIView):
    serializer_class = OrdersSerializer
    lookup_field = 'id'
    permission_classes = [IsOwnerOrReadOnly, IsAuthenticated]

    def get_queryset(self, *args, **kwargs):
        queryset = Checkout.objects.filter(user=self.request.user, status='waiting', id=self.kwargs['id']).order_by('-id')
        return queryset


class BuyOrdersAPIView(APIView):
    lookup_field = 'id'
    permission_classes = [IsOwnerOrReadOnly, IsAuthenticated]

    def post(self, request):
        username = self.request.user
        if username is None:
            raise Response({'message': ['you have not the permission to do that!']}, status=HTTP_400_BAD_REQUEST)
        else:
            account = Account.objects.filter(user=username)
            qs = Checkout.objects.filter(user=username, status='waiting')
            if account.exists():
                user = account.first()
                if user.gender is None \
                or user.country is None \
                or user.region is None \
                or user.address1 is None \
                or user.phone_number1 is None \
                or user.phone_number2 is None:
                    return Response(
                        {'message': ['add your information first to complete buy orders!']},
                        status=HTTP_200_OK
                    )
            if qs.exists():
                for order in qs:
                    order.status = 'pending'
                    order.save()
                    product = Product.objects.filter(id=order.product_id).first()
                    product.quantity -= order.quantity
                    product.number_of_sales += 1
                    product.save()
                return Response(
                        {'message': ['thank you for buying orders!']},
                        status=HTTP_200_OK
                    )
