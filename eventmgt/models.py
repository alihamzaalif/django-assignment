from django.db import models

# Create your models here.

class Category(models.Model):
    name = models.CharField(max_length=100)
    description = models.TextField(blank=True, null=True)

    def __str__(self):
        return self.name
    
class Event(models.Model):
    STATUS_CHOICES = [
        ('PENDING', 'Pending'),
        ('COMPLETED', 'Completed')
    ]
    name = models.CharField(max_length=100)
    description = models.TextField(blank=True, null=True)
    date = models.DateField()
    time = models.DateTimeField(auto_now=True)
    location = models.CharField(max_length=250)
    status = models.CharField(max_length=15, choices=STATUS_CHOICES, default="PENDING")
    category = models.ForeignKey(Category, on_delete=models.CASCADE, related_name='cat')

    def __str__(self):
        return self.name

class Participants(models.Model):
    name = models.CharField(max_length=100)
    email = models.EmailField(unique=True)
    event = models.ManyToManyField(Event,related_name='enrld')
    def __str__(self):
        return self.name