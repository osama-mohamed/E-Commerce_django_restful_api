from rest_framework.generics import (
    CreateAPIView,
    RetrieveAPIView,
    RetrieveUpdateAPIView,
    UpdateAPIView,
    DestroyAPIView,
)

from rest_framework.response import Response
from rest_framework.status import HTTP_200_OK, HTTP_400_BAD_REQUEST
from rest_framework.views import APIView
from rest_framework.permissions import IsAuthenticatedOrReadOnly, IsAdminUser, IsAuthenticated, AllowAny

from django.contrib.auth import get_user_model, update_session_auth_hash

from .serializers import (
    RegisterSerializer,
    LoginSerializer,
    ProfileSerializer,
    UpdateSerializer,
    ChangePasswordSerializer,
)
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


class ProfileAPIView(RetrieveAPIView):
    serializer_class = ProfileSerializer
    queryset = Account.objects.all()
    lookup_url_kwarg = 'id'
    lookup_field = 'id'
    permission_classes = [IsOwnerOrReadOnly, IsAuthenticated]


class ProfileUpdateAPIView(RetrieveUpdateAPIView):
    serializer_class = UpdateSerializer
    queryset = Account.objects.all()
    lookup_field = 'user'
    lookup_url_kwarg = 'id'
    permission_classes = [IsOwnerOrReadOnly, IsAuthenticated]


class ProfileDeleteAPIView(DestroyAPIView):
    serializer_class = ProfileSerializer
    queryset = User.objects.all()
    lookup_field = 'id'
    permission_classes = [IsOwnerOrReadOnly, IsAuthenticated]


class ChangePasswordAPIView(UpdateAPIView):
    serializer_class = ChangePasswordSerializer
    model = User
    permission_classes = [IsOwnerOrReadOnly, IsAuthenticated]

    def get_object(self):
        return self.request.user

    def update(self, request, *args, **kwargs):
        # self.object = self.get_object()
        user = self.get_object()
        serializer = self.get_serializer(data=request.data)
        # serializer = self.serializer_class(data=request.data)
        if serializer.is_valid():
            if not user.check_password(serializer.data.get("old_password")):
                return Response({"old_password": ["Wrong password"]}, status=HTTP_400_BAD_REQUEST)
            user.set_password(serializer.data.get("new_password"))
            user.save()
            update_session_auth_hash(request, user)
            return Response({'message': ['Success!']}, status=HTTP_200_OK)

        return Response(serializer.errors, status=HTTP_400_BAD_REQUEST)
