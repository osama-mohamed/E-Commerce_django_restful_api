from rest_framework.generics import (
    RetrieveAPIView,
    ListAPIView,
)

from rest_framework.filters import SearchFilter, OrderingFilter
from rest_framework.permissions import AllowAny

from django.db.models import Q

from .serializers import (
    ProductsSerializer,
    ProductDetailSerializer,
)

from products.models import Product
from .pagination import ProductPageNumberPagination


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