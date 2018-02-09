from rest_framework.serializers import ModelSerializer
from contact_us.models import ContactUs


class ContactUsSerializer(ModelSerializer):

    class Meta:
        model = ContactUs
        fields = [
            'username',
            'e_mail',
            'phone',
            'message',
        ]
