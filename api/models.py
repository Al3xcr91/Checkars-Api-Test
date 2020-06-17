from django.db import models

# Create your models here.

"""
  Test Models Checkars and Meli
"""

class CheckarsSite(models.Model):
  car_id = models.IntegerField(primary_key=True)
  _id = models.CharField(max_length=50)
  mlid = models.CharField(max_length=50)


class CheckarsSiteByID(models.Model):
  _id = models.CharField(primary_key=True, max_length=100)
  precio = models.FloatField()
  kilometros = models.IntegerField()


class MeliItem(models.Model):
  mlid = models.CharField(primary_key=True, max_length=50)
  status = models.CharField(max_length=10)
  precio = models.FloatField()
  kilometros = models.IntegerField()
  seller_id = models.IntegerField()
