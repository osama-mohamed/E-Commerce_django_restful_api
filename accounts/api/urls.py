from django.conf.urls import url
from .views import (
    RegisterAPIView,
    LoginAPIView,
    ProfileUpdateAPIView,
    )

urlpatterns = [
    # url(r'^activate/(?P<code>[a-zA-Z0-9].*)/$', activate_user_view, name='activate'),
    url(r'^register/', RegisterAPIView.as_view(), name='register_api'),
    url(r'^login/$', LoginAPIView.as_view(), name='login_api'),
    # url(r'^logout/$', UserLogoutView.as_view(), name='logout'),
    # url(r'^change_password/$', UserChangePasswordView.as_view(), name='change_password'),
    # url(r'^profile/$', UserProfileView.as_view(), name='profile'),
    url(r'^profile/update/(?P<id>\d+)/$', ProfileUpdateAPIView.as_view(), name='update_api'),
    # url(r'^profile/delete/$', ProfileDeleteView.as_view(), name='delete'),
]
