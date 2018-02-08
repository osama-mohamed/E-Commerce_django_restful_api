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


class RegisterSerializer(ModelSerializer):
    first_name = CharField(label='First name')
    last_name = CharField(label='Last name')
    username = CharField(label='Username')
    email = EmailField(label='E-mail')
    email_confirmation = EmailField(label='Confirm E-mail')
    password = CharField(label='Password')
    password_confirmation = CharField(label='Confirm Password')

    class Meta:
        model = User
        fields = [
            'first_name',
            'last_name',
            'username',
            'email',
            'email_confirmation',
            'password',
            'password_confirmation',
        ]
        extra_kwargs = {'password':
                            {'write_only': True}
                        }

    def create(self, validated_data):
        # username = self.validated_data.get('username')
        first_name = validated_data['first_name']
        last_name = validated_data['last_name']
        username = validated_data['username']
        email = validated_data['email']
        password = validated_data['password']
        user = User(
            first_name=first_name,
            last_name=last_name,
            username=username,
            email=email,
        )
        user.set_password(password)
        user.is_active = False
        user.save()
        user.account.send_activation_email()
        return validated_data

    def validate_username(self, username):
        qs = User.objects.filter(username__iexact=username)
        if qs.exists():
            raise ValidationError('This username is already registered before!')
        return username

    def validate_email_confirmation(self, email_confirmation):
        data = self.get_initial()
        email = data.get('email')
        # email_confirmation = data.get('email_confirmation')
        email_confirmation = email_confirmation
        if email != email_confirmation:
            raise ValidationError('Email dose not matched!')
        qs = User.objects.filter(email__iexact=email_confirmation)
        if qs.exists():
            raise ValidationError('This email is already registered before!')
        return email_confirmation

    def validate_password_confirmation(self, password_confirmation):
        data = self.get_initial()
        password = data.get('password')
        password_confirmation = password_confirmation
        if password != password_confirmation:
            raise ValidationError('Passwords dose not matched!')
        return password_confirmation


class LoginSerializer(ModelSerializer):
    username = CharField(label='Username', required=False, allow_blank=True)
    email = EmailField(label='E-mail', required=False, allow_blank=True)
    token = CharField(allow_blank=True, read_only=True)

    class Meta:
        model = User
        fields = [
            'username',
            'email',
            'password',
            'token',
        ]

    def validate(self, data):
        username = data.get('username', None)
        email = data.get('email', None)
        password = data.get('password')
        if not username and not email:
            raise ValidationError('Username or email are required for login!')
        user = User.objects.filter(
            Q(username=username, is_active=True) |
            Q(email=email, is_active=True)
        ).distinct()
        user = user.exclude(email__isnull=True).exclude(email__iexact='')
        if user.exists() and user.count() == 1:
            user_data = user.first()
        else:
            raise ValidationError('Username or Email is not valid!')
        if user_data:
            if not user_data.check_password(password):
                raise ValidationError('Incorrect Password!')
        data['token'] = 'random token is here for test'
        return data


class ProfileSerializer(ModelSerializer):
    edit_url = HyperlinkedIdentityField(
        view_name='accounts_api:update_api',
        lookup_field='id',
    )
    delete_url = HyperlinkedIdentityField(
        view_name='accounts_api:delete_api',
        lookup_field='id',
    )

    class Meta:
        model = Account
        fields = [
            'id',
            'edit_url',
            'delete_url',
            'first_name',
            'last_name',
            'username',
            'email',
            'gender',
            'country',
            'image',
            'region',
            'address1',
            'address2',
            'phone_number1',
            'phone_number2',
            'comments',
        ]


class UpdateSerializer(ModelSerializer):
    first_name = CharField(read_only=True)
    last_name = CharField(read_only=True)
    username = CharField(read_only=True)
    email = CharField(read_only=True)

    class Meta:
        model = Account
        fields = [
            'id',
            'first_name',
            'last_name',
            'username',
            'email',
            'gender',
            'country',
            'image',
            'region',
            'address1',
            'address2',
            'phone_number1',
            'phone_number2',
            'comments',
        ]

    def validate(self, data):
        gender = data.get('gender')
        country = data.get('country')
        region = data.get('region')
        address1 = data.get('address1')
        phone_number1 = data.get('phone_number1')
        phone_number2 = data.get('phone_number2')
        image = data.get('image')
        if not gender:
            raise ValidationError('Please select your gender!')
        if not country:
            raise ValidationError('Please enter your country!')
        if not region:
            raise ValidationError('Please enter your region!')
        if not address1:
            raise ValidationError('Please enter your address1!')
        if not phone_number1:
            raise ValidationError('Please enter your phone number1!')
        if not phone_number2:
            raise ValidationError('Please enter your phone number2!')
        if not image:
            raise ValidationError('You should upload an image!')
        return data


class ChangePasswordSerializer(Serializer):
    old_password = CharField(label='Old Password', required=True)
    new_password = CharField(label='New Password', required=True)
    new_password_confirmation = CharField(label='Confirm Password', required=True)

    def validate_new_password_confirmation(self, new_password_confirmation):
        data = self.get_initial()
        new_password = data.get('new_password')
        new_password_confirmation = new_password_confirmation
        if new_password != new_password_confirmation:
            raise ValidationError('Passwords dose not matched!')
        return new_password_confirmation
