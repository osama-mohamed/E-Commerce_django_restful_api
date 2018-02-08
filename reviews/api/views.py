from rest_framework.generics import (
    CreateAPIView,
    RetrieveUpdateAPIView,
    DestroyAPIView,
    ListAPIView,
)

from rest_framework.response import Response
from rest_framework.status import HTTP_200_OK, HTTP_400_BAD_REQUEST
from rest_framework.views import APIView
from rest_framework.permissions import IsAuthenticatedOrReadOnly, IsAuthenticated

from .serializers import (
    AddReviewSerializer,
)
from accounts.models import Account
from products.models import Product
from orders.models import Checkout
from reviews.models import Review
from .permissions import IsOwnerOrReadOnly


class AddReviewAPIView(APIView):
    serializer_class = AddReviewSerializer

    def post(self, request, *args, **kwargs):
        # print(new_data['rate'])
        # print(new_data['review'])
        # print(self.kwargs['id'])
        # print(request.user)
        # print(request.POST.get('rate'))
        # print(request.POST.get('review'))
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
            else:
                serializer = AddReviewSerializer(data=request.data)
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


