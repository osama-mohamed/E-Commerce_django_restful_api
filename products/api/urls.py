from django.conf.urls import url
from .views import (
    AllProductsAPIView,
    ProductsAPIView,
    ProductDetailAPIView,
    CategoryAPIView,
)

urlpatterns = [
    url(r'^category/(?P<category>[a-zA-Z0-9].*)/$', CategoryAPIView.as_view(), name='category_api'),
    url(r'^all/$', AllProductsAPIView.as_view(), name='all_api'),
    url(r'^(?P<slug>[\w-]+)/$', ProductDetailAPIView.as_view(), name='detail_api'),
    url(r'^$', ProductsAPIView.as_view(), name='list_api'),
]
