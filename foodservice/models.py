from django.contrib.auth.models import User
from django.core.exceptions import MultipleObjectsReturned
from django.db import models
from django.contrib.auth.backends import ModelBackend, UserModel


class EmailBackend(ModelBackend):
    def authenticate(self, request, username=None, password=None, **kwargs):
        try:
            user = UserModel.objects.get(email__iexact=username)
        except UserModel.DoesNotExist:
            UserModel().set_password(password)
        except MultipleObjectsReturned:
            return User.objects.filter(email=username).order_by('id').first()
        else:
            if user.check_password(password) and self.user_can_authenticate(user):
                return user

    def get_user(self, user_id):
        try:
            user = UserModel.objects.get(pk=user_id)
        except UserModel.DoesNotExist:
            return None

        return user if self.user_can_authenticate(user) else None


class Allergen(models.Model):
    name = models.CharField(
        max_length=25,
        verbose_name='Название алергена'
    )

    class Meta:
        verbose_name = 'аллерген'
        verbose_name_plural = 'аллергены'

    def __str__(self):
        return self.name


class Ingredient(models.Model):
    name = models.CharField(
        max_length=25,
        verbose_name="Название ингредиента"
    )

    class Meta:
        verbose_name = "Ингредиент"
        verbose_name_plural = "Ингредиенты"

    def __str__(self):
        return self.name


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
    name = models.CharField(
        max_length=50,
        verbose_name='Название рецепта'
    )
    calories = models.DecimalField(
        max_digits=7,
        decimal_places=2
    )
    proteins = models.DecimalField(
        max_digits=5,
        decimal_places=2,
        blank=True,
        null=True,
    )
    fats = models.DecimalField(
        max_digits=5,
        decimal_places=2,
        blank=True,
        null=True,
    )
    carbs = models.DecimalField(
        max_digits=5,
        decimal_places=2,
        blank=True,
        null=True,
    )
    image = models.ImageField(
        'картинка'
    )
    description = models.TextField(
        'описание',
        max_length=3000,
        blank=True,
    )
    category = models.ForeignKey(
        RecipeCategory,
        verbose_name='категория',
        related_name='recipes',
        null=True,
        blank=True,
        on_delete=models.SET_NULL,
    )
    allergens = models.ManyToManyField(
        Allergen,
        related_name='recipes_with_allergen',
        verbose_name='Алергены',
        blank=True)
    ingredients = models.ManyToManyField(
        Ingredient,
        through='RecipeIngredient',
        through_fields=('recipe', 'ingredient'),
    )

    class Meta:
        verbose_name = 'рецепт'
        verbose_name_plural = 'рецепты'

    def __str__(self):
        return self.name


class RecipeIngredient(models.Model):
    recipe = models.ForeignKey(
        Recipe,
        on_delete=models.CASCADE
    )
    ingredient = models.ForeignKey(
        Ingredient,
        on_delete=models.CASCADE
    )
    ingredient_quantity = models.IntegerField(
        blank=True,
        null=True,
        verbose_name='Количество ингредиента'
    )

    class Meta:
        verbose_name = 'ингредиенты рецепта'
        verbose_name_plural = 'ингредиенты рецепта'
