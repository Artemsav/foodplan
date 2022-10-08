from foodservice.models import Recipe, RecipeIngredient


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
