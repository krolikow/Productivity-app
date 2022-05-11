from django.db import models
from django.urls import reverse
#from users import models as mod

class Task(models.Model):
    DAYS = (
        ('M','Monday'),
        ('T','Tuesday'),
        ('W','Wednesday'),
        ('Th','Thursday'),
        ('F','Friday'),
        ('Sa','Saturday'),
        ('Su','Sunday'),
        ('X','Other'))

    title = models.CharField(max_length=200, null=True, blank=True)
    description = models.TextField(null = True, blank = True)
    complete = models.BooleanField(default=False)
    creation_date = models.DateTimeField(auto_now_add=True)
    day = models.CharField(max_length=15, choices=DAYS,default='X')
    #user = mod.ForeignKey(
        #User, on_delete=models.CASCADE, null=True, blank=True)
    # todo: due-date


    def __str__(self):
        return self.title 

    class Meta:
        ordering = ['complete']


class ShoppingList(models.Model):
    title = models.CharField(max_length = 50)

    def get_absolute_url(self):
        return reverse("list", args=[self.id])

    def __str__(self):
        return self.title
        
    class Meta:
        ordering = ['title',]
        
class Item(models.Model):
    title = models.CharField(max_length = 40)
    complete = models.BooleanField(default = False)
    shopping_list = models.ForeignKey(ShoppingList, on_delete=models.CASCADE)

    def get_absolute_url(self):
        return reverse(
            "item-update", args=[str(self.shopping_list.id), str(self.id)]
        )

    def __str__(self):
        return self.title
        
    class Meta:
        ordering = ['complete',]