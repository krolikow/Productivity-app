from django.db import models
from django.urls import reverse
from django.contrib.auth.models import User
from django.utils.timezone import localtime


class Tracker(models.Model):
    title = models.CharField(max_length = 40)

    def get_absolute_url(self):
        return reverse("tracker", args=[self.id])

    def __str__(self):
        return self.title


class Data(models.Model):
    # user = models.ForeignKey(to = User,on_delete=models.CASCADE)
    tracker = models.ForeignKey(Tracker, on_delete=models.CASCADE)
    title = models.CharField(max_length = 40)
    amount = models.FloatField()
    date = models.DateField(default = localtime)
    description = models.TextField(blank=True)
    created_at = models.DateTimeField(default=localtime)

    def __str__(self):
        return str(self.date ) + " " + str(self.amount)

    def get_absolute_url(self):
        return reverse('trackers:detail', kwargs={'pk': self.pk})
    
    class Meta:
        unique_together = 'tracker','date'
