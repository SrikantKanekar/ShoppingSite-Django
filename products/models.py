from django.db import models
from mptt.models import TreeForeignKey, MPTTModel
from django.utils.text import slugify
from django.contrib.auth.models import User
from django.db.models.signals import post_save
from django.dispatch import receiver
from django.utils import timezone


class Product(models.Model):
    title = models.CharField(max_length=100)
    category = TreeForeignKey('Category', null=True, blank=True, on_delete=models.CASCADE)
    image_url_1 = models.ImageField(upload_to='product/img', null=True, blank=True)
    image_url_2 = models.ImageField(upload_to='product/img', null=True, blank=True)
    image_url_3 = models.ImageField(upload_to='product/img', null=True, blank=True)
    offer_price = models.FloatField(default=0)
    original_price = models.FloatField(default=0)
    description = models.TextField(null=True, blank=True)
    quantity_left = models.IntegerField(null=True, blank=True)
    return_days = models.IntegerField(null=True, blank=True)
    slug = models.SlugField(unique=True, blank=True)

    def save(self, *args, **kwargs):
        self.slug = slugify(self.title)
        super(Product, self).save(*args, **kwargs)

    def get_product_id(self):
        return self.id

    def __str__(self):
        return self.title


class Category(MPTTModel):
    name = models.CharField(max_length=50, unique=True)
    parent = TreeForeignKey('self', null=True, blank=True, related_name='children', db_index=True,
                            on_delete=models.CASCADE)
    image_url = models.ImageField(upload_to='category/img', null=True, blank=True)
    description = models.CharField(max_length=200, null=True, blank=True)
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
            slugs.append('/'.join(ancestors[:i + 1]))
        return slugs

    def save(self, *args, **kwargs):
        self.slug = slugify(self.name)
        super(Category, self).save(*args, **kwargs)

    def __str__(self):
        return self.name


class Profile(models.Model):
    user = models.OneToOneField(User, on_delete=models.CASCADE)
    dp = models.ImageField(upload_to='profile/img', blank=True, null=True)
    country = models.CharField(max_length=20, blank=True, null=True)
    state = models.CharField(max_length=20, blank=True, null=True)
    city = models.CharField(max_length=20, blank=True, null=True)
    street_address = models.CharField(max_length=50, blank=True, null=True)
    postcode = models.IntegerField(blank=True, null=True)
    phone_number = models.IntegerField(blank=True, null=True)
    gender = models.CharField(choices=(('Male', 'Male'), ('Female', 'Female')), max_length=10, null=True, blank=True)
    wishlist_products = models.ManyToManyField(Product, blank=True, related_name='wishlist')
    cart_products = models.ManyToManyField(Product, blank=True)
    total_original = models.IntegerField(default=0)
    total_offer = models.IntegerField(default=0)
    total = models.IntegerField(default=0)

    def __str__(self):
        return self.user.username


@receiver(post_save, sender=User)
def create_user_profile(sender, instance, created, **kwargs):
    if created:
        Profile.objects.create(user=instance)


@receiver(post_save, sender=User)
def save_user_profile(sender, instance, **kwargs):
    instance.profile.save()


class Comment(models.Model):
    product = models.ForeignKey(Product, on_delete=models.CASCADE, related_name='comments', blank=True)
    user = models.ForeignKey(User, on_delete=models.CASCADE, blank=True)
    text = models.TextField()
    created_date = models.DateTimeField(default=timezone.now, blank=True)
    rating = models.CharField(max_length=5, blank=True, null=True)


order_status = [(0, 'Order Placed'),
                (1, 'Order Confirmed'),
                (2, 'Packing'),
                (3, 'Shipped'),
                (4, 'Out for Delivery'),
                (5, 'Delivered'),
                (6, 'Order Cancelled'),
                (7, 'Return Request Placed'),
                (8, 'Return Request Acknowledged'),
                (9, 'Courier Service Informed'),
                (10, 'Return Product Verified'),
                (11, 'Refund Completed')
                ]


class Admin(models.Model):
    ordered_product = models.ForeignKey(Product, on_delete=models.CASCADE, related_name='admin', blank=True)
    customer = models.ForeignKey(User, on_delete=models.CASCADE, blank=True)
    status = models.IntegerField(choices=order_status, default=0)

    order_placed_date = models.DateTimeField(default=timezone.now, blank=True, null=True)
    order_confirmed_date = models.DateTimeField(blank=True, null=True)
    packing_date = models.DateTimeField(blank=True, null=True)
    shipped_date = models.DateTimeField(blank=True, null=True)
    out_for_delivery_date = models.DateTimeField(blank=True, null=True)
    delivered_date = models.DateTimeField(blank=True, null=True)

    order_cancelled_date = models.DateTimeField(blank=True, null=True)

    return_request_placed_date = models.DateTimeField(blank=True, null=True)
    return_request_acknowledged_date = models.DateTimeField(blank=True, null=True)
    courier_service_informed_date = models.DateTimeField(blank=True, null=True)
    return_product_verified_date = models.DateTimeField(blank=True, null=True)
    refund_completed_date = models.DateTimeField(blank=True, null=True)

    def __str__(self):
        return '%s ==> %s ==> %s' % (self.customer.username, self.ordered_product.title, self.status)
