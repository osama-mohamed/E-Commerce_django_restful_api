from django.conf.urls import url
from .views import ContactUsAPIView

urlpatterns = [
    url(r'^$', ContactUsAPIView.as_view(), name='contact_us_api'),
]
