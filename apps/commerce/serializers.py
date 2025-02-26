from rest_framework import serializers

from apps.commerce.models import Product, Transaction


class ProductListSerializer(serializers.ModelSerializer):
    class Meta:
        model = Product
        fields = ('id', 'name', 'price', 'quantity')


class TransactionRequestSerializer(serializers.Serializer):
    product_id = serializers.IntegerField()
    quantity = serializers.IntegerField(min_value=1)
    money = serializers.DecimalField(max_digits=10, decimal_places=2, min_value=0)


class TransactionResponseSerializer(serializers.ModelSerializer):
    class Meta:
        model = Transaction
        fields = ('id', 'product', 'quantity', 'deposit', 'change', 'amount', 'created_dt', 'status')
