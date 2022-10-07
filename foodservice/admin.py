from django.contrib import admin
from foodservice.models import Allergen, Ingredient, RecipeCategory, Recipe, RecipeIngredient


class AllergenInline(admin.TabularInline):
    model = Recipe.allergens.through


class RecipeIngredientInline(admin.TabularInline):
    model = RecipeIngredient
    extra = 1


class AllergenAdmin(admin.ModelAdmin):
    inlines = [AllergenInline, ]


class RecipeAdmin(admin.ModelAdmin):
    list_display = ('name', 'calories', 'category',)
    inlines = [AllergenInline, RecipeIngredientInline]
    exclude = ('allergens',)


admin.site.register(Allergen, AllergenAdmin)
admin.site.register(Ingredient)
admin.site.register(RecipeCategory)
admin.site.register(Recipe, RecipeAdmin)
admin.site.register(RecipeIngredient)
