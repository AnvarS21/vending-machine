from django.db import models


class Product(models.Model):
    name = models.CharField('Название', max_length=255, help_text='Напишите название продукта')
    price = models.DecimalField('Цена', max_digits=10, decimal_places=2)
    quantity = models.PositiveIntegerField(default=0, verbose_name='Доступное количество')

    class Meta:
        verbose_name = 'Продукт'
        verbose_name_plural = 'Продукты'

    def __str__(self):
        return f'{self.name} - {self.price} р. - кол-во: {self.quantity}'


class Transaction(models.Model):
    product = models.ForeignKey(Product, on_delete=models.CASCADE, verbose_name='Продукт')
    quantity = models.PositiveIntegerField(default=1, verbose_name='Количество')
    amount = models.DecimalField('Сумма', max_digits=10, decimal_places=2)
    created_dt = models.DateTimeField('Время создания', auto_now_add=True)

    class Meta:
        verbose_name = 'Транзакция'
        verbose_name_plural = 'Транзакции'

    def __str__(self):
        return f'{self.product.name} -{self.amount}'
