from django.contrib import admin
from .models import Item,Task,ShoppingList

admin.site.register(Task)
admin.site.register(ShoppingList)
admin.site.register(Item)