from decimal import Decimal

from django.test import TestCase

from apps.commerce.exceptions import InsufficientProductQuantityError, InsufficientFundsError
from apps.commerce.models import Product
from apps.commerce.services import VendingMachineService
from apps.commerce.choices import TransactionStatuses
from apps.commerce.models import Transaction


class VendingMachineServiceTests(TestCase):
    def setUp(self):
        self.first_product = Product.objects.create(
            name='Лимонад',
            price=Decimal('110.0'),
            quantity=102,
        )
        self.second_product = Product.objects.create(
            name='Энергетик',
            price=Decimal('85.0'),
            quantity=0,
        )

    def test_available_products(self):
        products = VendingMachineService.get_available_products()
        self.assertEqual(products.count(), 1)

    def test_get_product(self):
        product = VendingMachineService.get_product(1)
        self.assertEqual(product.name, 'Лимонад')
        self.assertEqual(product.price, Decimal('110.0'))
        self.assertEqual(product.quantity, 102)

    def test_check_quantity(self):
        with self.assertRaises(InsufficientProductQuantityError):
            VendingMachineService.check_quantity(self.first_product, 1000)

    def test_check_deposit(self):
        with self.assertRaises(InsufficientFundsError):
            requested_quantity = 5
            VendingMachineService.check_deposit(10, self.first_product.price * requested_quantity)

    def test_purchase_product_insufficient_quantity(self):
        product_id = self.first_product.id
        purchase_quantity = 1000
        money_inserted = Decimal('600.0')

        with self.assertRaises(InsufficientProductQuantityError):
            VendingMachineService.purchase_product(product_id, purchase_quantity, money_inserted)

        self.first_product.refresh_from_db()
        self.assertEqual(self.first_product.quantity, 102)

        self.assertEqual(Transaction.objects.count(), 0)

    def test_purchase_product_insufficient_funds(self):
        product_id = self.first_product.id
        purchase_quantity = 10
        product_price = self.first_product.price
        total_price = product_price * purchase_quantity
        money_inserted = Decimal('50.0')

        with self.assertRaises(InsufficientFundsError):
            VendingMachineService.purchase_product(product_id, purchase_quantity, money_inserted)

        self.first_product.refresh_from_db()
        self.assertEqual(self.first_product.quantity, 102)

        self.assertEqual(Transaction.objects.count(), 0)

    def test_purchase_product(self):
        product_id = self.first_product.id
        initial_quantity = self.first_product.quantity
        purchase_quantity = 5
        product_price = self.first_product.price
        total_price = product_price * purchase_quantity
        money_inserted = Decimal('600.0')

        result = VendingMachineService.purchase_product(product_id, purchase_quantity, money_inserted)

        self.first_product.refresh_from_db()

        self.assertEqual(self.first_product.quantity, initial_quantity - purchase_quantity)


        transaction = Transaction.objects.last()
        self.assertIsNotNone(transaction)
        self.assertEqual(transaction.product.id, product_id)
        self.assertEqual(transaction.quantity, purchase_quantity)
        self.assertEqual(transaction.deposit, money_inserted)
        self.assertEqual(transaction.amount, total_price)
        self.assertEqual(transaction.change, money_inserted - total_price)
        self.assertEqual(transaction.status, TransactionStatuses.SUCCESS)

        expected_result = {
            'product': product_id,
            'quantity': purchase_quantity,
            'deposit': money_inserted,
            'change': money_inserted - total_price,
            'amount': total_price,
            'status': TransactionStatuses.SUCCESS
        }
        self.assertEqual(result, expected_result)
