from rest_framework.generics import (
    CreateAPIView,
    RetrieveAPIView,
    RetrieveUpdateAPIView,
    UpdateAPIView,
    DestroyAPIView,
    ListAPIView,
)

from rest_framework.filters import SearchFilter, OrderingFilter
from rest_framework.response import Response
from rest_framework.status import HTTP_200_OK, HTTP_400_BAD_REQUEST
from rest_framework.views import APIView
from rest_framework.permissions import IsAuthenticatedOrReadOnly, IsAdminUser, IsAuthenticated, AllowAny

from django.contrib.auth import get_user_model, update_session_auth_hash
from django.db.models import Q
from .serializers import (
    ProductsSerializer,
    ProductDetailSerializer,
)
from products.models import Product
from .permissions import IsOwnerOrReadOnly
from .pagination import ProductPageNumberPagination

User = get_user_model()


class AllProductsAPIView(ListAPIView):
    serializer_class = ProductsSerializer
    # queryset = Product.objects.all().order_by('-id')
    pagination_class = ProductPageNumberPagination
    permission_classes = [AllowAny, ]

    def get_queryset(self, *args, **kwargs):
        queryset = Product.objects.filter(publish=True).order_by('-id')
        return queryset


class ProductsAPIView(ListAPIView):
    serializer_class = ProductsSerializer
    # queryset = Product.objects.all().order_by('-id')
    filter_backends = [SearchFilter, OrderingFilter]
    search_fields = ['name', 'description']
    permission_classes = [AllowAny, ]

    def get_queryset(self, *args, **kwargs):
        queryset = Product.objects.filter(publish=True).order_by('-id')
        query = self.request.GET.get('search')
        if query:
            queryset = Product.objects.filter(
                                              Q(name__icontains=query) |
                                              Q(description__icontains=query)
                                              , publish=True).distinct()
        return queryset


class ProductDetailAPIView(RetrieveAPIView):
    serializer_class = ProductDetailSerializer
    # queryset = Product.objects.all().order_by('-id')
    lookup_field = 'slug'
    permission_classes = [AllowAny, ]

    def get_queryset(self, *args, **kwargs):
        queryset = Product.objects.filter(slug__iexact=self.kwargs['slug'], publish=True)
        return queryset


class CategoryAPIView(ListAPIView):
    serializer_class = ProductsSerializer
    # queryset = Product.objects.all().order_by('-id')
    pagination_class = ProductPageNumberPagination
    permission_classes = [AllowAny, ]

    def get_queryset(self, *args, **kwargs):
        queryset = Product.objects.filter(publish=True, category__category=self.kwargs['category']).order_by('-id')
        return queryset