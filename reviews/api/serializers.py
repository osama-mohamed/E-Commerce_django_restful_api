from rest_framework.serializers import (
    ModelSerializer,
    ValidationError,
)
from reviews.models import Review


class ReviewSerializer(ModelSerializer):

    class Meta:
        model = Review
        fields = [
            'rate',
            'review',
        ]

    def validate_rate(self, rate):
        if not rate:
            raise ValidationError('Rate is required!')
        return rate

    def validate_review(self, review):
        if not review:
            raise ValidationError('review is required!')
        return review
