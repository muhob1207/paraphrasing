from django.db import models
from django.urls import reverse

# Create your models here.
class Phrase(models.Model):
    text = models.CharField(max_length=250)

    def __str__(self):
        return self.text
    
    def get_absolute_url(self):
        return reverse('phrase_detail', kwargs={'pk':self.pk})
