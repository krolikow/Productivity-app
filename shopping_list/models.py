from django.urls import reverse
from django.db import models


class ShoppingList(models.Model):
    title = models.CharField(max_length=50)

    def get_absolute_url(self):
        return reverse("list", args=[self.id])

    def __str__(self):
        return self.title

    class Meta:
        ordering = ['title', ]


class Item(models.Model):
    title = models.CharField(max_length=40)
    complete = models.BooleanField(default=False)
    shopping_list = models.ForeignKey(ShoppingList, on_delete=models.CASCADE)

    def get_absolute_url(self):
        return reverse(
            "item-update", args=[str(self.shopping_list.id), str(self.id)]
        )

    def __str__(self):
        return self.title

    class Meta:
        ordering = ['complete', ]
