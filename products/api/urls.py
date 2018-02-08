from django.conf.urls import url
from .views import (
    ProductsAPIView,
    ProductDetailAPIView,
)

urlpatterns = [
    # url(r'^category/(?P<category>[a-zA-Z0-9].*)/$', CategoryListView.as_view(), name='category'),
    # url(r'^all/$', AllProductsListView.as_view(), name='all'),
    url(r'^(?P<slug>[\w-]+)/$', ProductDetailAPIView.as_view(), name='detail_api'),
    url(r'^$', ProductsAPIView.as_view(), name='list_api'),
]
