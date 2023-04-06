from django.views.decorators.http import require_GET
from drf_spectacular.openapi import AutoSchema
from drf_yasg.utils import swagger_auto_schema
from rest_framework import status
from rest_framework.decorators import permission_classes, api_view
from rest_framework.generics import CreateAPIView, get_object_or_404
from rest_framework.permissions import IsAuthenticated
from rest_framework.views import APIView
from rest_framework.response import Response
from .models import ProductCategory, Product
from .serializers import ProductSerializer,ProductCategorySerializer



class ProductListCreateView(CreateAPIView):
    serializer_class = ProductSerializer
    permission_classes = [IsAuthenticated]

    def post(self, request, format=None, **kwargs):
        if not isinstance(request.data, list):
            data = [request.data]
        else:
            data = request.data
        serializer = self.get_serializer(data=data, many=True,context={'request':request.method})
        if serializer.is_valid():
            for instance in serializer.validated_data:
                serializer = self.get_serializer(data=instance,context={'request':request.method})
                if serializer.is_valid():
                    serializer.save()
                else:
                    return Response(serializer.errors, status=status.HTTP_400_BAD_REQUEST)
            return Response(serializer.data, status=status.HTTP_201_CREATED)
        return Response(serializer.errors, status=status.HTTP_400_BAD_REQUEST)

class ProductUpdateView(APIView):
    
    serializer_class = ProductSerializer
    permission_classes = [IsAuthenticated]

    @swagger_auto_schema(
        request_body=ProductSerializer,
        responses={status.HTTP_200_OK: ProductSerializer()},
    )
    def put(self, request, id, format=None):
        product = get_object_or_404(Product, id=id)
        serializer = ProductSerializer(product, data=request.data, context={'request': request.method})
        if serializer.is_valid():
            serializer.save()
            return Response(serializer.data)
        return Response(serializer.errors, status=status.HTTP_400_BAD_REQUEST)


class ProductListView(APIView):
    
    serializer_class = ProductSerializer
    def get(self, request, format=None, **kwargs):
        id = kwargs.get('id', None)
        name = kwargs.get('name', None)

        if id:
            product = get_object_or_404(Product, id=id)
            serializer = ProductSerializer(product, context={'request': request.method})
        elif name:
            product = Product.objects.filter(name__icontains=name)
            serializer = ProductSerializer(product, many=True,context={'request': request.method})
        else:
            products = Product.objects.all()
            serializer = ProductSerializer(products, many=True,context={'request':request.method})
        return Response(serializer.data,status=status.HTTP_200_OK)


class ProductDeleteView(APIView):
    
    permission_classes = [IsAuthenticated]

    def delete(self, request, id, format=None):
        product = get_object_or_404(Product, id=id)
        product.delete()
        return Response(status=status.HTTP_204_NO_CONTENT)


class ProductCategoryListCreateView(APIView):
    serializer_class = ProductCategorySerializer
    def get(self, request, format=None):
        categories = ProductCategory.objects.all()
        serializer = ProductCategorySerializer(categories, many=True)
        return Response(serializer.data)

    @permission_classes([IsAuthenticated])
    def post(self, request, format=None):
        serializer = ProductCategorySerializer(data=request.data)
        if serializer.is_valid():
            serializer.save()
            return Response(serializer.data, status=status.HTTP_201_CREATED)
        return Response(serializer.errors, status=status.HTTP_400_BAD_REQUEST)
