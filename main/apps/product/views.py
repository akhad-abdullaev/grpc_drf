from rest_framework import generics 
from .models import Product
from .serializer import ProductCreateSerializer, ProductSerializer
from ..common.pagination import CustomPagination
from rest_framework import permissions
from rest_framework_simplejwt import authentication



class ProductListCreateAPIView(generics.ListCreateAPIView):
    queryset = Product.objects.all()
    pagination_class = CustomPagination
    # authentication_classes = [authentication.JWTAuthentication]
    # permission_classes = [permissions.IsAuthenticated]

    def get_serializer_class(self):
        if self.request.method == 'POST':
            return ProductCreateSerializer
        else:
            return ProductSerializer

product_list_create_api_view = ProductListCreateAPIView.as_view()



class ProductDetailView(generics.RetrieveUpdateDestroyAPIView):
    queryset = Product.objects.all()
    serializer_class = ProductSerializer
    # authentication_classes = [authentication.JWTAuthentication]
    # permission_classes = [permissions.IsAuthenticated]

product_retrieve_update_delete_api_view = ProductDetailView.as_view()
