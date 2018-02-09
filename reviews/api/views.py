from rest_framework.generics import DestroyAPIView
from rest_framework.response import Response
from rest_framework.status import HTTP_200_OK, HTTP_400_BAD_REQUEST
from rest_framework.views import APIView
from rest_framework.permissions import IsAuthenticated

from .serializers import (
    ReviewSerializer,
)
from accounts.models import Account
from products.models import Product
from reviews.models import Review
from .permissions import IsOwnerOrReadOnly


class AddReviewAPIView(APIView):
    serializer_class = ReviewSerializer
    permission_classes = [IsAuthenticated]

    def post(self, request, *args, **kwargs):
        id = self.kwargs['id']
        user = self.request.user
        if user.is_authenticated:
            product = Product.objects.filter(id=id, publish=True).first()
            if product.block_review is True:
                return Response(
                    {'message': ['This product is blocked for adding review products!']},
                    status=HTTP_400_BAD_REQUEST
                )
            user = Account.objects.filter(user=self.request.user).first()
            if user.block_review is True:
                return Response(
                    {'message': ['You blocked from adding review products!']},
                    status=HTTP_400_BAD_REQUEST
                )
            qs = Review.objects.filter(user=self.request.user, product=product)
            if qs.exists():
                return Response(
                    {'message': ['You can not add this product review because you already added a review before!']},
                    status=HTTP_400_BAD_REQUEST
                )
            if request.POST.get('review') == '' or request.POST.get('rate') is None:
                return Response(
                    {'message': ['You must write a valid product review!']},
                    status=HTTP_400_BAD_REQUEST
                )
            else:
                serializer = ReviewSerializer(data=request.data)
                if serializer.is_valid():
                    new_data = serializer.data
                    new_review = Review.objects.create(
                        user=self.request.user,
                        product=product,
                        review=new_data['review'],
                        rate=new_data['rate'],
                    )
                    products = Review.objects.filter(product_id=id)
                    summition_rate = 0
                    products_length = 0
                    for pro in products:
                        summition_rate += pro.rate
                        products_length += 1
                    avg = summition_rate / products_length
                    avg_rate = Product.objects.get(id=id)
                    avg_rate.avg_rate = avg
                    avg_rate.save()
                    return Response(
                        {'message': ['Successfully added your product review!']},
                        status=HTTP_200_OK
                    )
        else:
            return Response(
                {'message': ['You do not have permission to do that!']},
                status=HTTP_400_BAD_REQUEST
            )


class UpdateReviewAPIView(APIView):
    serializer_class = ReviewSerializer
    permission_classes = [IsOwnerOrReadOnly, IsAuthenticated]

    def get_queryset(self, *args, **kwargs):
        queryset = Review.objects.all()
        return queryset

    def post(self, request, *args, **kwargs):
        id = self.kwargs['id']
        user = self.request.user
        if user.is_authenticated:
            product = Product.objects.filter(id=id, publish=True).first()
            if product.block_review is True:
                return Response(
                    {'message': ['This product is blocked for editing review products!']},
                    status=HTTP_400_BAD_REQUEST
                )
            user = Account.objects.filter(user=self.request.user).first()
            if user.block_review is True:
                return Response(
                    {'message': ['You blocked from editing review products!']},
                    status=HTTP_400_BAD_REQUEST
                )
            if request.POST.get('review') == '' or request.POST.get('rate') is None:
                return Response(
                    {'message': ['You must write a valid product review!']},
                    status=HTTP_400_BAD_REQUEST
                )
            else:
                serializer = ReviewSerializer(data=request.data)
                if serializer.is_valid():
                    new_data = serializer.data
                    qs = Review.objects.filter(user=self.request.user, product=product).first()
                    qs.review = new_data['review']
                    qs.rate = new_data['rate']
                    qs.save()
                    products = Review.objects.filter(product_id=id)
                    summition_rate = 0
                    products_length = 0
                    for pro in products:
                        summition_rate += pro.rate
                        products_length += 1
                    avg = summition_rate / products_length
                    avg_rate = Product.objects.get(id=id)
                    avg_rate.avg_rate = avg
                    avg_rate.save()
                    return Response(
                        {'message': ['Successfully updated your product review!']},
                        status=HTTP_200_OK
                    )
        else:
            return Response(
                {'message': ['You do not have permission to do that!']},
                status=HTTP_400_BAD_REQUEST
            )


class DeleteReviewAPIView(DestroyAPIView):
    serializer_class = ReviewSerializer
    lookup_field = 'id'
    permission_classes = [IsOwnerOrReadOnly, IsAuthenticated]

    def delete(self, request, *args, **kwargs):
        user = self.request.user
        id = self.kwargs['id']
        if user.is_authenticated:
            product = Product.objects.filter(id=id).first()
            if product.block_review is True:
                return Response(
                    {'message': ['This product is blocked for deleting review products!']},
                    status=HTTP_400_BAD_REQUEST
                )
            user = Account.objects.filter(user=self.request.user).first()
            if user.block_review is True:
                return Response(
                    {'message': ['You blocked from deleting review products!']},
                    status=HTTP_400_BAD_REQUEST
                )
            queryset = Review.objects.filter(user=self.request.user, product_id=self.kwargs['id'])
            if queryset.exists() and queryset.count() == 1:
                review = queryset.first()
                review.delete()
                products = Review.objects.filter(product_id=id)
                summition_rate = 0
                products_length = 0
                for pro in products:
                    summition_rate += pro.rate
                    products_length += 1
                try:
                    avg = summition_rate / products_length
                except ZeroDivisionError:
                    avg = 0
                avg_rate = Product.objects.get(id=id)
                avg_rate.avg_rate = avg
                avg_rate.save()
                return Response(
                    {'message': ['Successfully deleted your product review!']},
                    status=HTTP_400_BAD_REQUEST
                )
        else:
            return Response(
                {'message': ['You do not have permission to do that!']},
                status=HTTP_400_BAD_REQUEST
            )
