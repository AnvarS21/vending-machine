from apps.commerce.choices import TransactionStatuses
from apps.commerce.exceptions import ProductNotFoundError, InsufficientProductQuantityError, InsufficientFundsError
from apps.commerce.models import Product, Transaction
from django.db import transaction


class VendingMachineService:
    @staticmethod
    def get_available_products():
        return Product.objects.filter(quantity__gt=0)

    @staticmethod
    def get_product(product_id):
        try:
            product = Product.objects.select_for_update().get(id=product_id)
        except Product.DoesNotExist:
            raise ProductNotFoundError(f"Товар с ID {product_id} не найден")
        return product

    @staticmethod
    def check_quantity(product, quantity):
        if product.quantity < quantity:
            raise InsufficientProductQuantityError(
                f"Недостаточно товара. Запрошено: {quantity}, В наличии: {product.quantity}"
            )

    @staticmethod
    def check_deposit(money_inserted, total_price):
        if money_inserted < total_price:

            raise InsufficientFundsError(
                f"Недостаточно денег. Требуется: {total_price}, Внесено: {money_inserted}"
            )

    @staticmethod
    @transaction.atomic
    def purchase_product(product_id, quantity, money_inserted):
        product = VendingMachineService.get_product(product_id)
        total_price = product.price * quantity
        try:

            VendingMachineService.check_quantity(product, quantity)
            VendingMachineService.check_deposit(money_inserted, total_price)

            change = money_inserted - total_price

            product.quantity -= quantity
            product.save()

            transaction_obj = Transaction.objects.create(
                product=product,
                quantity=quantity,
                deposit=money_inserted,
                change=change,
                amount=total_price,
                status=TransactionStatuses.SUCCESS
            )

            return transaction_obj
        except Exception:
            Transaction.objects.create(
                product=product,
                quantity=quantity,
                deposit=money_inserted,
                change=money_inserted,
                amount=0,
                status=TransactionStatuses.ERROR
            )
            raise