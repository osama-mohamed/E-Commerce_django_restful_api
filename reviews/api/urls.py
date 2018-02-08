from django.conf.urls import url
from .views import (
    AddReviewAPIView,
    UpdateReviewAPIView,
    DeleteReviewAPIView,
)

urlpatterns = [
    url(r'^add_review/(?P<id>\d+)/$', AddReviewAPIView.as_view(), name='add_api'),
    url(r'^update_review/(?P<id>\d+)/$', UpdateReviewAPIView.as_view(), name='update_api'),
    url(r'^delete_review/(?P<id>\d+)/$', DeleteReviewAPIView.as_view(), name='delete_api'),
]
