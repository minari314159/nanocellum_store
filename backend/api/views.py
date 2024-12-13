from django.shortcuts import get_object_or_404
from django.contrib.auth.models import User
from rest_framework.generics import CreateAPIView, ListCreateAPIView, RetrieveUpdateDestroyAPIView
from rest_framework.mixins import CreateModelMixin, RetrieveModelMixin, DestroyModelMixin
from rest_framework.viewsets import GenericViewSet, ModelViewSet
from rest_framework.response import Response
from rest_framework import status
from .serializers import CartSerializer, ReviewSerializer, UserSerializer, ProductSerializer, CartItemSerializer
from .models import Cart, CartItem, Product, Review
from rest_framework.permissions import IsAuthenticatedOrReadOnly, AllowAny, IsAdminUser

# Create your views here.


class ProductViewSet(ModelViewSet):
    queryset = Product.objects.all()
    serializer_class = ProductSerializer

    def get_serializer_context(self):
        return {'request': self.request}

    def get_permissions(self):
        """
        Set permissions dynamically:
        - Allow anyone for GET requests.
        - Require admin privileges for POST, PUT, DELETE.
        """
        if self.request.method == 'GET':
            return [AllowAny()]
        return [IsAdminUser()]

    def delete(self, request, pk):
        product = get_object_or_404(Product, pk=pk)
        if product.orderitems.count() > 0:
            return Response({'error': 'Product cannot be deleted because it is associated with an order item.'}, status=status.HTTP_405_METHOD_NOT_ALLOWED)
        product.delete()
        return Response(status=status.HTTP_204_NO_CONTENT)


class ProductDetail(RetrieveUpdateDestroyAPIView):
    queryset = Product.objects.all()
    serializer_class = ProductSerializer
    lookup_field = 'id'

    def get_permissions(self):
        """
        Set permissions dynamically:
        - Allow anyone for GET requests.
        - Require admin privileges for POST, PUT, DELETE.
        """
        if self.request.method == 'GET':
            return [AllowAny()]
        return [IsAdminUser()]

    def delete(self, request, id):
        """Delete a product (admin only)."""
        product = get_object_or_404(Product, pk=id)
        product.delete()
        return Response(
            {"detail": "Product deleted successfully."},
            status=status.HTTP_204_NO_CONTENT)


class ReviewViewSet(ModelViewSet):
    serializer_class = ReviewSerializer

    def get_queryset(self):
        return Review.objects.filter(product_id=self.kwargs['product_pk'])

    def get_serializer_context(self):
        return {'product_id': self.kwargs['product_pk']}


class CreateUserView(CreateAPIView):
    queryset = User.objects.all()
    serializer_class = UserSerializer
    permission_classes = [AllowAny]


class CartViewSet(CreateModelMixin,
                  RetrieveModelMixin,
                  DestroyModelMixin,
                  GenericViewSet):
    queryset = Cart.objects.prefetch_related('items__product').all()
    serializer_class = CartSerializer
    permission_classes = [AllowAny]


class CartItemViewSet(ModelViewSet):
    http_method_names = ['get', 'post', 'patch', 'delete']
    permission_classes = [AllowAny]

    def get_serializer_class(self):
        if self.request.method == 'POST':
            pass
            # return AddCartItemSerializer
        elif self.request.method == 'PATCH':
            pass
            # return UpdateCartItemSerializer
        return CartItemSerializer

    def get_serializer_context(self):
        return {'cart_id': self.kwargs['cart_pk']}

    def get_queryset(self):
        return CartItem.objects \
            .filter(cart_id=self.kwargs['cart_pk']) \
            .select_related('product')
