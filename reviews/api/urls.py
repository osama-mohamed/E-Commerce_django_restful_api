from django.conf.urls import url
from .views import (
    AddReviewAPIView,
)

urlpatterns = [
    url(r'^add_review/(?P<id>\d+)/$', AddReviewAPIView.as_view(), name='add_api'),
    # url(r'^update_review/(?P<id>\d+)/$', UpdateReviewView.as_view(), name='update'),
    # url(r'^delete_review/(?P<id>\d+)/$', DeleteReviewView.as_view(), name='delete'),
]
