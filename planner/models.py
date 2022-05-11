from django.db import models
from django.urls import reverse
from django.contrib.auth.models import User
from django.utils.timezone import localtime

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





class Tracker(models.Model):
    title = models.CharField(max_length = 40)

    def __str__(self):
        return self.title


class Data(models.Model):
	user = models.ForeignKey(to = User,on_delete=models.CASCADE)
	amount = models.FloatField()
	date = models.DateField(default = localtime)
	description = models.TextField()
	created_at = models.DateTimeField(default=localtime)

	def __str__(self):
		return str(self.date )+ str(self.amount)
