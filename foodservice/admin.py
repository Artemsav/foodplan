from django.contrib import admin
from foodservice.models import Allergen, Ingredient, RecipeCategory, MenuType, Recipe, RecipeIngredient, SubscriptionType


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


class SubscriptionTypeAdmin(admin.ModelAdmin):
    list_display = ('name', 'term', 'price',)


admin.site.register(SubscriptionType, SubscriptionTypeAdmin)
admin.site.register(Allergen, AllergenAdmin)
admin.site.register(Ingredient)
admin.site.register(RecipeCategory)
admin.site.register(MenuType)
admin.site.register(Recipe, RecipeAdmin)
admin.site.register(RecipeIngredient)
