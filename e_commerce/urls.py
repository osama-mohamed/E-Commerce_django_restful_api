from django.conf.urls import url, include
from django.contrib import admin

from django.conf import settings
from django.conf.urls.static import static

from products.urls import ProductsListView


urlpatterns = [
    url(r'^admin/', admin.site.urls),
    url(r'^accounts/', include('accounts.urls', namespace='accounts')),
    url(r'^products/', include('products.urls', namespace='products')),
    url(r'^orders/', include('orders.urls', namespace='orders')),
    url(r'^reviews/', include('reviews.urls', namespace='reviews')),
    url(r'^contact_us/', include('contact_us.urls', namespace='contact_us')),
    url(r'^$', ProductsListView.as_view(), name='main_home'),


    url(r'^api/accounts/', include('accounts.api.urls', namespace='accounts_api')),
    url(r'^api/products/', include('products.api.urls', namespace='products_api')),
    url(r'^api/orders/', include('orders.api.urls', namespace='orders_api')),
    url(r'^api/reviews/', include('reviews.api.urls', namespace='reviews_api')),
    url(r'^api/contact_us/', include('contact_us.api.urls', namespace='contact_us_api')),

]# + static(settings.STATIC_URL, document_root=settings.STATIC_ROOT)


urlpatterns += static(settings.STATIC_URL, document_root=settings.STATIC_ROOT)
urlpatterns += static(settings.MEDIA_URL, document_root=settings.MEDIA_ROOT)
