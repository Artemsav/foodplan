from django.contrib import admin

from foodservice.models import User, Allergen, Ingredient, RecipeCategory, Recipe, RecipeIngredient

class RecipeAdmin(admin.ModelAdmin):
	raw_id_fields = ('ingredients',)

admin.site.register(User)
admin.site.register(Allergen)
admin.site.register(Ingredient)
admin.site.register(RecipeCategory)
admin.site.register(Recipe, RecipeAdmin)
admin.site.register(RecipeIngredient)
