from django.db import models


# Create your models here.

class EWasteSite(models.Model):
    site_id = models.CharField(max_length=10)
    name = models.CharField(max_length=100)
    ownership = models.CharField(max_length=10)
    site = models.CharField(max_length=50)

    def __str__(self):
        return self.name

class Clothing(models.Model):
    name = models.CharField(max_length=100)
    address = models.CharField(max_length=100)
    district = models.CharField(max_length=50)

    def __str__(self):
        return self.name