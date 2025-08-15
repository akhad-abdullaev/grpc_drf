from rest_framework import serializers 
from .models import Product
from ..category.serializer import CategorySerializer


class ProductSerializer(serializers.ModelSerializer):
    class Meta:
        model = Product
        fields = (
            'id',
            'guid',
            'category',
            'title',
            'price',
            'description'
        )
    
    def to_representation(self, instance):
        self.fields['category'] = CategorySerializer()
        data = super().to_representation(instance)
        return data


class ProductCreateSerializer(serializers.ModelSerializer):
    class Meta:
        model = Product
        fields = (
            'category',
            'title',
            'price',
            'description'
        )


# class ProductMaterialSerializer(serializers.ModelSerializer):
#     # product_materials = WarehouseSerializer()
#     class Meta:
#         model = ProductMaterial
#         fields = (
#             'id',
#             'product',
#             'quantity',
#             'material'
#         )
    
#     def to_representation(self, instance):
#         self.fields['product_materials'] = WarehouseSerializer()
#         data = super().to_representation(instance)
#         return data
