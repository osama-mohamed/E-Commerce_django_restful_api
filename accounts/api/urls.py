from django.conf.urls import url
from .views import (
    RegisterAPIView,
    LoginAPIView,
    ProfileAPIView,
    ProfileUpdateAPIView,
    ProfileDeleteAPIView,
    ChangePasswordAPIView,
    )

urlpatterns = [
    url(r'^register/', RegisterAPIView.as_view(), name='register_api'),
    url(r'^login/$', LoginAPIView.as_view(), name='login_api'),
    url(r'^change_password/$', ChangePasswordAPIView.as_view(), name='change_password_api'),
    url(r'^profile/(?P<id>\d+)/$', ProfileAPIView.as_view(), name='profile_api'),
    url(r'^profile/update/(?P<id>\d+)/$', ProfileUpdateAPIView.as_view(), name='update_api'),
    url(r'^profile/delete/(?P<id>\d+)/$', ProfileDeleteAPIView.as_view(), name='delete_api'),
]
