from django.db import models

CATEGORIES = (
    ('1', 'fruits'),
    ('2', 'vegetables')
)


class Product(models.Model):
    category = models.CharField(choices=CATEGORIES, max_length=1)
    name = models.CharField(max_length=100)
    price = models.FloatField()
    description = models.TextField()
    image_url_1 = models.CharField(max_length=2083)
    image_url_2 = models.CharField(max_length=2083)
    image_url_3 = models.CharField(max_length=2083)
    quantity_left = models.IntegerField()
    return_days = models.IntegerField()
