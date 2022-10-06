from django.contrib import admin
from foodservice.models import User, Allergie, RecipeCategory, Recipe

admin.site.register(User)
admin.site.register(Allergie)
admin.site.register(RecipeCategory)
admin.site.register(Recipe)

