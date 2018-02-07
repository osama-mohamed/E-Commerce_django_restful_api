from rest_framework.serializers import (
    ModelSerializer,
    CharField,
    EmailField,
    ValidationError,
    )

from django.contrib.auth import get_user_model

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
        username = validated_data['username']
        email = validated_data['email']
        password = validated_data['password']
        user = User(
            username=username,
            email=email,
        )
        user.set_password(password)
        user.save()
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
