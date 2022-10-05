from django.db import models
from django.utils import timezone


class Subscription(models.Model):
    name = models.CharField('Название подписки')
    status = models.BooleanField(
        'Статус подписки',
        default=False,
        db_index=True
    )
    start_at = models.DateTimeField(
        'Дата оформления подписки',
        default=timezone.now,
        db_index=True
        )
    ended_at = models.DateTimeField(
        'Дата окончания подписки',
        default=timezone.now,
        db_index=True
        )