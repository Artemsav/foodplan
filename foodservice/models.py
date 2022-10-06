from django.db import models
from django.core.validators import MinValueValidator


class User(models.Model):
    username = models.CharField(max_length=25, verbose_name='Имя пользователя')
    coocking_for = models.IntegerField(
        'На скольких готовим',
        validators=[MinValueValidator(0)]
    )

    class Meta:
        verbose_name = 'пользователь'
        verbose_name_plural = 'пользователи'

    def __str__(self):
        return self.username


class Allergen(models.Model):
    name = models.CharField(max_length=25, verbose_name='Название алергена')

    class Meta:
        verbose_name = 'аллерген'
        verbose_name_plural = 'аллергены'

    def __str__(self):
        return self.name


class Ingredient(models.Model):
    name = models.CharField(max_length=25, verbose_name="Название ингредиента")

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
    name = models.CharField(max_length=50, verbose_name='Название рецепта')
    calories = models.DecimalField(max_digits=7, decimal_places=2)
    proteins = models.DecimalField(
        max_digits=5, decimal_places=2, blank=True, null=True,)
    fats = models.DecimalField(
        max_digits=5, decimal_places=2, blank=True, null=True,)
    carbs = models.DecimalField(
        max_digits=5, decimal_places=2, blank=True, null=True,)
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
    recipe = models.ForeignKey(Recipe, on_delete=models.CASCADE)
    ingredient = models.ForeignKey(Ingredient, on_delete=models.CASCADE)
    ingredient_quantity = models.IntegerField(
        blank=True,
        null=True,
        verbose_name='Количество ингредиента'
    )

    class Meta:
        verbose_name = 'ингредиенты рецепта'
        verbose_name_plural = 'ингредиенты рецепта'
