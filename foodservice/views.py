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
        'description': recipe.description,
        'image_url' : recipe.image.url
    }


def selected_recipes(sub):
    recipes = Recipe.objects.exclude(allergens__in=sub.allergens.all())
    if sub.breakfast:
        breakfast_receipe = recipes.filter(category__name='Завтрак').order_by('?')[:1]
    else:
        breakfast_receipe = Recipe.objects.none()
    if sub.dinner:
        dinner_receipe = recipes.filter(category__name='Обед').order_by('?')[:1]
    else:
        dinner_receipe = Recipe.objects.none()
    if sub.supper:
        supper_receipe = recipes.filter(category__name='Ужин').order_by('?')[:1]
    else:
        supper_receipe = Recipe.objects.none()
    if sub.desert:
        desert_receipe =  recipes.filter(category__name='Десерт').order_by('?')[:1]
    else:
        desert_receipe = Recipe.objects.none()           
    return breakfast_receipe | dinner_receipe | supper_receipe | desert_receipe


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
                   serialize_recipe(recipe) for recipe in selected_recipes(sub)
               ]
               }
    return render(request, template_name="lk.html", context=context)


def register_user(request):
    context = {}
    if request.method == 'POST':
        form = request.POST
        if not User.objects.filter(email=form['email']).exists():
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
