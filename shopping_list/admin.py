from django.contrib import admin
from shopping_list.models import ShoppingList,Item


admin.site.register(ShoppingList)
admin.site.register(Item)