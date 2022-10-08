from django.shortcuts import render

from foodservice.models import (Allergen, Recipe, RecipeIngredient,
                                SubscriptionType)


def serialize_recipe(recipe):
    ingredients = RecipeIngredient.objects.filter(recipe=recipe)
    serialized_ingredients = []
    for ingredient in ingredients:
        serialized_ingredients.append({
            'name': ingredient.ingredient.name,
            'quantity': ingredient.ingredient_quantity,
        })
    return {
        'category': recipe.category.name,
        'name': recipe.name,
        'calories': recipe.calories,
        'ingridients': serialized_ingredients,
    }


def selected_recipes(allergen, menu_types):
    return Recipe.objects.order_by('?')[:3]


def card(request):
    context = {
        'selected_recipes': [
            serialize_recipe(recipe) for recipe in selected_recipes(1, 1)
        ]
    }
    return (request, 'card1.html', context)


def get_subscription(request):
    terms = set(
        sub_type.term for sub_type
        in SubscriptionType.objects.order_by('-term')
    )
    allergens = set(
        (allergen.name, allergen.id) for allergen in Allergen.objects.all()
    )
    context = {
        'subscription_options': {
            'terms': terms,
            'allergens': allergens
        }
    }
    if request.method == 'POST':
        # добавление подписки в БД
        pass
    return render(request, template_name="order.html", context=context)
