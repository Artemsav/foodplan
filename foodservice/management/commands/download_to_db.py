import json
from foodservice.models import Recipe, Ingredient, RecipeIngredient, RecipeCategory
from django.core.management.base import BaseCommand
import re

class Command(BaseCommand):

    def handle(self, *args, **options):
        try:
            load_to_db()
        except Exception as exc:
            raise


def load_to_db():
    with open('result.json', 'r', encoding="utf-8") as file:
        recipies = json.loads(file.read())
        all_ingredients = Ingredient.objects.all()
        all_categories = RecipeCategory.objects.all()
        all_ingredients_list = [ing.name for ing in all_ingredients]
        all_categories_list = [cat.name for cat in all_categories]
        for recipe_title, recipe_description in recipies.items():
                for category in recipe_description.get('categorys'):
                    if category not in all_categories_list:
                        RecipeCategory.objects.create(name=category) 
                description = ' \n'.join(recipe_description.get('steps'))
                new_recipe = Recipe.objects.create(
                    name=recipe_title, calories=300,
                    image=recipe_description.get('image_url'),
                    description=description,
                    category=RecipeCategory.objects.filter(name__contains=recipe_description.get('categorys')[0])[0]
                )            
                for ing in recipe_description.get('ingredients'):
                    linked_ingr = Ingredient.objects.filter(name__contains=ing[0], ingredient_quantity__contains=int(ing[1]))[0]
                    if ing[0] not in all_ingredients_list:
                        linked_ingr = Ingredient.objects.create(name=ing[0])
                    try:
                        product, amount, measer = ing
                        match = re.match(r'([0-9]+)-([0-9]+)', amount, re.I)
                        if match:
                            minim, maxi = match.groups()
                            median_v = (int(minim)+int(maxi))/2
                            RecipeIngredient.objects.create(recipe=new_recipe, ingredient=linked_ingr, ingredient_quantity=int(median_v), ingredient_measure=ing[2])
                    except Exception as err:
                        product, measer = ing
                        amount = 0  
                        RecipeIngredient.objects.create(recipe=new_recipe, ingredient=linked_ingr, ingredient_quantity=int(amount), ingredient_measure=ing[2])                
                    try:
                        RecipeIngredient.objects.create(recipe=new_recipe, ingredient=linked_ingr, ingredient_quantity=int(amount), ingredient_measure=ing[2])
                    except Exception as err:
                        print(f'error {err}'
