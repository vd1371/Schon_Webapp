from django.db import models
from django.core.validators import MaxValueValidator, MinValueValidator

from .Participant import Participant
from .Stock import Stock

# Create your models here.
class Shareholding(models.Model):
    
    participant = models.ForeignKey(Participant, on_delete= models.CASCADE)
    stock = models.ForeignKey(Stock, on_delete= models.CASCADE)
    name = models.CharField(max_length = 200)
    address = models.CharField(max_length= 400)
    shareholding = models.PositiveIntegerField()
    percentage = models.FloatField(validators=[MinValueValidator(0.0),
                                                MaxValueValidator(100.0)])
    date = models.DateTimeField()

