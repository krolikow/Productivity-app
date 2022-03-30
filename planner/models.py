from django.db import models


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
    # todo: due-date

    def __str__(self):
        return self.title 

    class Meta:
        ordering = ['complete']
