from rest_framework.serializers import (
    ModelSerializer,
    Serializer,
    CharField,
    EmailField,
    ValidationError,
    HyperlinkedIdentityField,
    )

from django.contrib.auth import get_user_model
from django.db.models import Q

from accounts.models import Account

User = get_user_model()

