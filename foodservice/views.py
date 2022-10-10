from django.contrib.auth.models import User
from django.http import HttpResponseRedirect
from django.shortcuts import render
from django.urls import reverse

from foodservice.models import (Allergen, Recipe, RecipeCategory,
                                RecipeIngredient)
from subscription.models import Subscription


def serialize_recipe(recipe):
    ingredients = RecipeIngredient.objects.filter(recipe=recipe)
    serialized_ingredients = []
    for ingredient in ingredients:
        serialized_ingredients.append(
            f'{ingredient.ingredient.name}, {str(ingredient.ingredient_quantity)} г')

    return {
        'category': recipe.category.name,
        'name': recipe.name,
        'calories': recipe.calories,
        'ingridients': serialized_ingredients,
        'description': recipe.description
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


def get_account(request):
    if not Subscription.objects.filter(client=request.user, status=True).exists():
        context = {
            'subscription_status': 0
        }
        return render(request, template_name="lk.html", context=context)
    sub = Subscription.objects.get(client=request.user, status=True)
    allergens = [allergen.name for allergen in sub.allergens.all()]

    # br_ingridients_context = []
    # receipts = {}
    # breakfast_receipe = RecipeCategory.objects.get(name='Завтрак')\
    #     .recipes.order_by('?').first()
    # breakfast_ingridients = breakfast_receipe.ingredients.all()
    # br_ingridients_context = [ingridient.name for ingridient
    #                           in breakfast_ingridients]

    context = {'subscription':
               {'name': sub.type.name,
                   'status': 1,
                   'paid_till': sub.paid_till,
                   'allergens': allergens,
                   'dishes': sub.dishes,
                   'breakfast': sub.breakfast,
                   'dinner': sub.dinner,
                   'supper': sub.supper,
                   'desert': sub.desert
                },
               'selected_recipes': [
                   # в функцию будем передавать данные подписки, она возвращает рецепты
                   serialize_recipe(recipe) for recipe in selected_recipes(1, 1)
               ]
               }
    return render(request, template_name="lk.html", context=context)


def register_user(request):
    context = {}
    if request.method == 'POST':
        form = request.POST
        if not User.objects.filter(username=form['username']).exists():
            user = User.objects.create_user(
                username=form['username'],
                password=form['password'],
                email=form['email']
            )
            user.save()
            return HttpResponseRedirect(reverse('login'))
        else:
            context = {
                'error': 'Такой пользователь существует'
            }
    return render(request, template_name="registration.html", context=context)
