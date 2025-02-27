from decimal import Decimal

from django.urls import reverse
from rest_framework import status
from rest_framework.test import APITestCase

from apps.commerce.models import Product, Transaction
from apps.commerce.choices import TransactionStatuses


class ProductListViewTests(APITestCase):
    def setUp(self):
        self.url = reverse('products-list')

        self.product1 = Product.objects.create(
            name='Лимонад',
            price=Decimal('110.0'),
            quantity=102,
        )
        self.product2 = Product.objects.create(
            name='Энергетик',
            price=Decimal('85.0'),
            quantity=0,
        )
        self.product3 = Product.objects.create(
            name='Шоколадка',
            price=Decimal('50.0'),
            quantity=25,
        )

    def test_list_available_products(self):
        response = self.client.get(self.url)

        self.assertEqual(response.status_code, status.HTTP_200_OK)
        self.assertEqual(len(response.data), 2)

        product_ids = [item['id'] for item in response.data]
        self.assertIn(self.product1.id, product_ids)
        self.assertIn(self.product3.id, product_ids)
        self.assertNotIn(self.product2.id, product_ids)
        product_data = next(item for item in response.data if item['id'] == self.product1.id)
        self.assertEqual(product_data['name'], 'Лимонад')
        self.assertEqual(Decimal(product_data['price']), Decimal('110.0'))
        self.assertEqual(product_data['quantity'], 102)


class TransactionViewSetTests(APITestCase):
    def setUp(self):
        self.url = reverse('vending-purchase')
        self.product = Product.objects.create(
            name='Лимонад',
            price=Decimal('110.0'),
            quantity=102,
        )

        self.unavailable_product = Product.objects.create(
            name='Энергетик',
            price=Decimal('85.0'),
            quantity=0,
        )

    def test_successful_purchase(self):
        initial_quantity = self.product.quantity

        data = {
            'product_id': self.product.id,
            'quantity': 5,
            'money': '600.00'
        }

        response = self.client.post(self.url, data, format='json')

        self.assertEqual(response.status_code, status.HTTP_200_OK)
        self.assertEqual(response.data['product'], self.product.id)
        self.assertEqual(response.data['quantity'], 5)
        self.assertEqual(Decimal(response.data['deposit']), Decimal('600.00'))
        self.assertEqual(Decimal(response.data['amount']), Decimal('550.00'))
        self.assertEqual(Decimal(response.data['change']), Decimal('50.00'))
        self.assertEqual(response.data['status'], TransactionStatuses.SUCCESS)

        self.product.refresh_from_db()
        self.assertEqual(self.product.quantity, initial_quantity - 5)

        transaction = Transaction.objects.last()
        self.assertIsNotNone(transaction)
        self.assertEqual(transaction.product.id, self.product.id)
        self.assertEqual(transaction.quantity, 5)

    def test_product_not_found(self):
        data = {
            'product_id': 999,
            'quantity': 1,
            'money': '200.00'
        }

        response = self.client.post(self.url, data, format='json')

        self.assertEqual(response.status_code, status.HTTP_404_NOT_FOUND)
        self.assertIn('error', response.data)

    def test_insufficient_quantity(self):
        data = {
            'product_id': self.product.id,
            'quantity': 500,
            'money': '60000.00'
        }

        response = self.client.post(self.url, data, format='json')

        self.assertEqual(response.status_code, status.HTTP_400_BAD_REQUEST)
        self.assertIn('error', response.data)
        self.assertEqual(response.data['status'], TransactionStatuses.ERROR)

        initial_quantity = self.product.quantity
        self.product.refresh_from_db()
        self.assertEqual(self.product.quantity, initial_quantity)

    def test_insufficient_funds(self):
        data = {
            'product_id': self.product.id,
            'quantity': 5,
            'money': '100.00'
        }

        response = self.client.post(self.url, data, format='json')

        self.assertEqual(response.status_code, status.HTTP_400_BAD_REQUEST)
        self.assertIn('error', response.data)
        self.assertEqual(response.data['status'], TransactionStatuses.ERROR)

        initial_quantity = self.product.quantity
        self.product.refresh_from_db()
        self.assertEqual(self.product.quantity, initial_quantity)

    def test_invalid_request_data(self):
        data = {
            'product_id': self.product.id,
            'money': '500.00'
        }

        response = self.client.post(self.url, data, format='json')

        self.assertEqual(response.status_code, status.HTTP_400_BAD_REQUEST)
        self.assertIn('error', response.data)
        self.assertIn('details', response.data)
