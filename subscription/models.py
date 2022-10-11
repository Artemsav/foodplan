
from django.db import models
from foodservice.models import Allergen, User, MenuType


class SubscriptionType(models.Model):
    name = models.CharField(
        max_length=35
    )
    term = models.IntegerField(
        verbose_name='Срок подписки',
    )
    price = models.IntegerField()

    class Meta:
        verbose_name = 'тип подписки'
        verbose_name_plural = 'типы подписки'

    def __str__(self):
        return self.name


class Subscription(models.Model):
    client = models.ForeignKey(
        User,
        on_delete=models.CASCADE,
        verbose_name='Клиент',
        related_name='subscritions',
    )
    dishes = models.IntegerField(
        verbose_name='Количество блюд',
    )
    created_at = models.TimeField(
        verbose_name='Дата создания',
        auto_now_add=True,
    )
    paid_till = models.TimeField(
        verbose_name='Оплачено до',
        blank=True,
        null=True
    )
    status = models.BooleanField(
        verbose_name='Активна',
        default=True
    )
    type = models.ForeignKey(
        SubscriptionType,
        on_delete=models.SET_NULL,
        verbose_name='Тип подписки',
        related_name='subscriptions',
        null=True
    )
    menu_type = models.ForeignKey(
        MenuType,
        on_delete=models.SET_NULL,
        verbose_name='Тип меню',
        related_name='subscriptions',
        null=True
    )
    breakfast = models.BooleanField(
        verbose_name='Завтрак',
        default=True
    )
    dinner = models.BooleanField(
        verbose_name='Обед',
        default=True)
    supper = models.BooleanField(
        verbose_name='Ужин',
        default=True
    )
    desert = models.BooleanField(
        verbose_name='Десерт',
        default=True
    )
    allergens = models.ManyToManyField(
        Allergen,
        related_name='subscriptions',
        verbose_name='Алергены',
        blank=True
    )
    price_total = models.IntegerField()

    class Meta:
        verbose_name = 'подписка'
        verbose_name_plural = 'подписки'

    def __str__(self):
        return str(self.type)