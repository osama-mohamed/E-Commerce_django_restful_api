from rest_framework.generics import (
    CreateAPIView,
    RetrieveAPIView,
    RetrieveUpdateAPIView,
    DestroyAPIView,
)

from rest_framework.response import Response
from rest_framework.status import HTTP_200_OK, HTTP_400_BAD_REQUEST
from rest_framework.views import APIView
from rest_framework.permissions import IsAuthenticatedOrReadOnly, IsAdminUser, IsAuthenticated, AllowAny

from django.contrib.auth import get_user_model

from .serializers import RegisterSerializer, LoginSerializer, UpdateSerializer
from accounts.models import Account
from .permissions import IsOwnerOrReadOnly

User = get_user_model()


class RegisterAPIView(CreateAPIView):
    serializer_class = RegisterSerializer
    queryset = ''
    permission_classes = [AllowAny, ]


class LoginAPIView(APIView):
    serializer_class = LoginSerializer
    permission_classes = [AllowAny, ]

    def post(self, request):
        serializer = LoginSerializer(data=request.data)
        if serializer.is_valid(raise_exception=True):
            new_data = serializer.data
            return Response(new_data, status=HTTP_200_OK)
        return Response(serializer.errors, status=HTTP_400_BAD_REQUEST)


class ProfileUpdateAPIView(RetrieveUpdateAPIView):
    serializer_class = UpdateSerializer
    queryset = Account.objects.all()
    lookup_field = 'user'
    lookup_url_kwarg = 'id'
    permission_classes = [IsOwnerOrReadOnly, IsAuthenticated, IsAdminUser]
