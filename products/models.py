from django.db import models
from mptt.models import TreeForeignKey, MPTTModel
from django.utils.text import slugify


class Product(models.Model):
    title = models.CharField(max_length=100)
    category = TreeForeignKey('Category', null=True, blank=True, on_delete=models.CASCADE)
    price = models.FloatField()
    description = models.TextField()
    image_url_1 = models.CharField(max_length=2083)
    image_url_2 = models.CharField(max_length=2083)
    image_url_3 = models.CharField(max_length=2083)
    quantity_left = models.IntegerField()
    return_days = models.IntegerField()
    slug = models.SlugField(unique=True, blank=True)

    def save(self, *args, **kwargs):
        self.slug = slugify(self.title)
        super(Product, self).save(*args, **kwargs)

    def __str__(self):
        return self.title


class Category(MPTTModel):
    name = models.CharField(max_length=50, unique=True)
    parent = TreeForeignKey('self', null=True, blank=True, related_name='children', db_index=True, on_delete=models.CASCADE)
    image_url = models.CharField(max_length=2083, null=True, blank=True)
    description = models.CharField(max_length=100, null=True, blank=True)
    slug = models.SlugField(unique=True, blank=True)

    class MPTTMeta:
        order_insertion_by = ['name']

    class Meta:
        unique_together = ('parent', 'slug')
        verbose_name_plural = 'categories'

    def get_slug_list(self):
        try:
            ancestors = self.get_ancestors(include_self=True)
        except:
            ancestors = []
        else:
            ancestors = [i.slug for i in ancestors]
        slugs = []
        for i in range(len(ancestors)):
            slugs.append('/'.join(ancestors[:i+1]))
        return slugs

    def save(self, *args, **kwargs):
        self.slug = slugify(self.name)
        super(Category, self).save(*args, **kwargs)

    def __str__(self):
        return self.name
