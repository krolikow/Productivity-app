from django.urls import reverse
from django.db import models
from django.contrib.auth.models import User

class ShoppingList(models.Model):
    title = models.CharField(max_length=50)
    user = models.ForeignKey(User,on_delete=models.CASCADE, null=True, blank=True)

    def get_absolute_url(self):
        return reverse("list", args=[self.id])

    def __str__(self):
        return self.title

    class Meta:
        ordering = ['title', ]



class Item(models.Model):
    class Unit(models.TextChoices):
        PIECE = "piece", "PIECE"
        KG = "kg", "KG"
        DAG = "dag" , "DAG"
        G = "g" , "G"

    class Category(models.TextChoices):
        DRINKS = "drinks", "DRINKS"
        DAIRY = "dairy", "DAIRY"
        DESSERT = "dessert", "DESSERT"
        FRUIT = "fruit", "FRUIT"
        GRAINS = "grains" , "GRAINS"
        MEAT = "meat", "MEAT"
        VEGETABLES = "vegetables", "VEGETABLES"

    title = models.CharField(max_length=40)
    complete = models.BooleanField(default=False)
    shopping_list = models.ForeignKey(ShoppingList, on_delete=models.CASCADE)
    amount = models.FloatField()
    unit = models.CharField(max_length=20,choices=Unit.choices, default=Unit.PIECE)
    category = models.CharField(max_length=100,choices=Category.choices,default=Category.DRINKS)
    
    def get_absolute_url(self):
        return reverse(
            "item-update", args=[str(self.shopping_list.id), str(self.id)]
        )

    def __str__(self):
        return self.title

    class Meta:
        ordering = ['complete', ]


