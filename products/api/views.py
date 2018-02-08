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

from django.contrib.auth import get_user_model, update_session_auth_hash

from .serializers import (
    ProductsSerializer,
    ProductDetailSerializer,
)
from products.models import Product
from .permissions import IsOwnerOrReadOnly

User = get_user_model()


class ProductsAPIView(ListAPIView):
    serializer_class = ProductsSerializer
    # queryset = Product.objects.all().order_by('-id')
    permission_classes = [AllowAny, ]

    def get_queryset(self, *args, **kwargs):
        queryset = Product.objects.filter(publish=True)
        return queryset


class ProductDetailAPIView(RetrieveAPIView):
    serializer_class = ProductDetailSerializer
    # queryset = Product.objects.all().order_by('-id')
    lookup_field = 'slug'
    permission_classes = [AllowAny, ]

    def get_queryset(self, *args, **kwargs):
        queryset = Product.objects.filter(slug__iexact=self.kwargs['slug'], publish=True)
        return queryset
