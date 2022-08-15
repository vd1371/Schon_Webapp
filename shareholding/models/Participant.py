from django.db import models

# Create your models here.
class Participant(models.Model):
    
    id = models.CharField(primary_key=True, max_length = 10, unique = True)
    name = models.CharField(max_length = 100)