from rest_framework import serializers
from rest_framework.exceptions import ValidationError

from .models import Product, Stock, StockProduct


class ProductSerializer(serializers.ModelSerializer):
    class Meta:
        model = Product
        fields = ['id', 'title', 'description']


class ProductPositionSerializer(serializers.ModelSerializer):
    class Meta:
        model = StockProduct
        fields = ['product', 'quantity', 'price']


class StockSerializer(serializers.ModelSerializer):
    positions = ProductPositionSerializer(many=True)

    class Meta:
        model = Stock
        fields = ['id', 'address', 'positions']

    def validate_positions(self, value):
        if not value:
            raise ValidationError('Нужны позиции на складе')
        products = [pos.get('product') for pos in value]
        if len(products) != len(set(products)):
            raise ValidationError('Повторение продуктов')
        return value

    def create(self, validated_data):
        positions = validated_data.pop('positions')
        stock = super().create(validated_data)
        for position in positions:
            StockProduct.objects.create(stock=stock, **position)
        return stock

    def update(self, instance, validated_data):
        positions = validated_data.pop('positions')
        instance.positions.all().delete()
        for position in positions:
            StockProduct.objects.update_or_create(stock=instance, **position)
        return instance
