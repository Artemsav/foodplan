from django.db import models
from django.core.validators import MinValueValidator


class User(models.Model):
    username = models.CharField('Имя пользователя')
    coocking_for = models.IntegerField(
        'На скольких готовим',
        validators=[MinValueValidator(0)]
    )

    class Meta:
        verbose_name = 'ресторан'
        verbose_name_plural = 'рестораны'

    def __str__(self):
        return self.username


class Allergie(models.Model):
    name = models.CharField('Название алергии')
    allergic_users = models.ManyToManyField(
        User,
        verbose_name='Аллергии',
        related_name='allergies',
        null=True,
        blank=True,
        on_delete=models.SET_NULL,
    )


class RecipeCategory(models.Model):
    name = models.CharField(
        'название',
        max_length=50
    )

    class Meta:
        verbose_name = 'категория'
        verbose_name_plural = 'категории'

    def __str__(self):
        return self.name


class Recipe(models.Model):
    name = models.CharField('Название рецепта')
    calories = models.DecimalField(max_digits=7, decimal_places=2)
    proteins = models.DecimalField(max_digits=5, decimal_places=2)
    fats = models.DecimalField(max_digits=5, decimal_places=2)
    carbs = models.DecimalField(max_digits=5, decimal_places=2)
    image = models.ImageField(
        'картинка'
    )
    category = models.ForeignKey(
        RecipeCategory,
        verbose_name='категория',
        related_name='recipes',
        null=True,
        blank=True,
        on_delete=models.SET_NULL,
    )
    description = models.TextField(
        'описание',
        max_length=200,
        blank=True,
    )
