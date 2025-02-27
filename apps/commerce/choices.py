from django.db import models


class TransactionStatuses(models.TextChoices):
    SUCCESS = ('success', 'Успешно')
    ERROR = ('error', 'Ошибка')
