

from rest_framework import serializers
from .models import Product, ProductCategory

class ProductSerializer(serializers.ModelSerializer):
    combined_price = serializers.SerializerMethodField()

    class Meta:
        model = Product
        fields = ('id','name', 'price', 'currency', 'rank', 'product_category','created_time','combined_price')

    def get_combined_price(self, obj):
        return f"{obj.price} {obj.currency.upper()}"

    def create(self, validated_data):
        product_data = validated_data
        product_instance = []
        product_instance=Product(**product_data)
        product_instance.save()
        return product_instance

    def to_representation(self, instance):
        # Remove 'created_time' field from serializer output for POST requests
        if self.context['request'] == 'POST':
            self.fields.pop('created_time')
            self.fields.pop('combined_price')
        elif self.context['request'] == 'GET':
            if 'id' in self.fields:
                self.fields.pop('id')
            if 'rank' in self.fields:
                self.fields.pop('rank')
            if 'currency' in self.fields:
                self.fields.pop('currency')


        data = super().to_representation(instance)
        if 'combined_price' in data:
            data['price'] = data['combined_price']
            del data['combined_price']
        return data

    def to_internal_value(self, data):
        if isinstance(data.get('product_category'), ProductCategory):
            data['product_category'] = data['product_category'].pk
        return super().to_internal_value(data)



class ProductCategorySerializer(serializers.ModelSerializer):
    class Meta:
        model = ProductCategory
        fields = '__all__'