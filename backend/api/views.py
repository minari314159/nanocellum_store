from django_filters.rest_framework import DjangoFilterBackend
from rest_framework.mixins import CreateModelMixin, RetrieveModelMixin, DestroyModelMixin
from rest_framework.decorators import action
from rest_framework.viewsets import ModelViewSet, GenericViewSet
from rest_framework.response import Response
from rest_framework.filters import SearchFilter, OrderingFilter
from rest_framework.pagination import PageNumberPagination
from rest_framework.permissions import IsAuthenticated, IsAdminUser
from .permissions import IsAdminOrReadOnly, ViewCustomerHistoryPermission
from .models import *
from .serializers import *
from .filters import ProductFilter


# -------------------------------Product CRUD ----------------------------------#
class ProductsViewSet(ModelViewSet):
    queryset = Product.objects.prefetch_related('images').all()
    serializer_class = ProductSerializer
    permission_classes = [IsAdminOrReadOnly]
# allows the user to filter the products by color by redifining the get_queryset method
    filter_backends = [DjangoFilterBackend, SearchFilter, OrderingFilter]
    filterset_class = ProductFilter
    pagination_class = PageNumberPagination
    # allows the user to search for products by name or description, case insensitive
    search_fields = ['name', 'description']
    ordering_fields = ['price']

# provides the request to the serializer to automatically associate the product with the user
    def get_serializer_context(self):
        return {'request': self.request}

# allows the user to delete a product only if it is not associated with an orderitem
    def destroy(self, request, *args, **kwargs):

        if OrderItem.objects.filter(product_id=kwargs['pk']).count() > 0:
            return Response({'error': 'Product cannot be deleted because its associated with an orderitem pending'})

        return super().destroy(request, *args, **kwargs)


class ProductImageViewSet(ModelViewSet):
    serializer_class = ProductImageSerializer

    # provides the product_id to the serializer to automatically associate the product image with the product
    def get_serializer_context(self):
        return {'product_id': self.kwargs['product_pk']}

    # where self.kwargs['product_pk'] is the product id from the url path
    def get_queryset(self):
        return ProductImage.objects.filter(product_id=self.kwargs['product_pk'])

 # -------------------------------Review CRUD ----------------------------------#


class ReviewViewSet(ModelViewSet):
    serializer_class = ReviewSerializer
    # allows the user to only see the reviews for a specific product in the url path

    def get_queryset(self):
        return Review.objects.filter(product_id=self.kwargs['product_pk'])
# provides the product_id to the serializer to automatically associate the review with the product

    def get_serializer_context(self):
        return {'product_id': self.kwargs['product_pk']}

# -------------------------------CART CRUD ----------------------------------#


class CartViewSet(CreateModelMixin,
                  RetrieveModelMixin,
                  DestroyModelMixin,
                  GenericViewSet):
    # prefetch_related allows the user to see the cart items in the cart view without making additional unnecessary queries to the database
    # 'items__product' retrieves the product associated with the cart item so dont't have separate queries for each cart item
    queryset = Cart.objects.prefetch_related('items__product').all()
    serializer_class = CartSerializer


class CartItemViewSet(ModelViewSet):
    http_method_names = ['get', 'post', 'patch', 'delete']
    # override serializer class to create dynamic use of serializer class based on the request method

    def get_serializer_class(self):
        if self.request.method == 'POST':
            return AddToCartSerializer
        elif self.request.method == 'PATCH':
            return UpdateCartItemSerializer
        return CartItemSerializer

    # provides the cart_id to the serializer to automatically associate the cart item with the cart
    def get_serializer_context(self):
        return {'cart_id': self.kwargs['cart_pk']}

    # allows the user to only see the cart items for a specific cart in the url path will allow to see cart items without other cart properties like id

    def get_queryset(self):
        return CartItem.objects\
            .filter(cart_id=self.kwargs['cart_pk'])\
            .select_related('product')

# -----------------------------Customer CRUD ----------------------------------#


class CustomerViewSet(ModelViewSet):
    queryset = Customer.objects.all()
    serializer_class = CustomerSerializer
    permission_classes = [IsAdminUser]

    @action(detail=True, permission_classes=[ViewCustomerHistoryPermission])
    def history(self, request, pk):
        return Response({'message': 'History endpoint reached'})
# allows the user to only see the customer associated with the user in the url path

    @action(detail=False, methods=['GET', 'PUT'], permission_classes=[IsAuthenticated])
    def me(self, request):
        customer = Customer.objects.get(
            user_id=request.user.id)
        if request.method == 'GET':
            serializer = CustomerSerializer(customer)
            return Response(serializer.data)
        elif request.method == 'PUT':
            serializer = CustomerSerializer(customer, data=request.data)
            serializer.is_valid(raise_exception=True)
            serializer.save()
            return Response(serializer.data)


# -------------------------------Order CRUD ----------------------------------#


class OrderViewSet(ModelViewSet):
    ordering_fields = ['placed_at']
    http_method_names = ['get', 'post', 'patch', 'delete', 'head', 'options']

    def get_permissions(self):
        if self.request.method in ['PATCH', 'DELETE']:
            return [IsAdminUser()]
        return [IsAuthenticated()]

    def create(self, request, *args, **kwargs):
        serializer = CreateOrderSerializer(data=request.data, context={
                                           'user_id': self.request.user.id})
        serializer.is_valid(raise_exception=True)
        order = serializer.save()
        serializer = OrderSerializer(order)
        return Response(serializer.data)

    # create dynamic use of serializer class based on the request method
    def get_serializer_class(self):
        if self.request.method == 'POST':
            return CreateOrderSerializer
        elif self.request.method == 'PATCH':
            return UpdateOrderSerializer
        return OrderSerializer

    # allows the user to only see the orders associated with the user in the url path
    def get_queryset(self):
        user = self.request.user
        if user.is_staff:
            return Order.objects.all()

        customer_id = Customer.objects.only(
            'id').get(user_id=user.id)
        return Order.objects.filter(customer_id=customer_id)
