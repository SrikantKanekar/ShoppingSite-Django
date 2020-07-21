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
    first_name = models.CharField(max_length=100, blank=True, null=True)
    last_name = models.CharField(max_length=100, blank=True, null=True)
    email = models.CharField(max_length=100, blank=True, null=True)
    dp = models.ImageField(upload_to='profile/img', null=True)
    country = models.CharField(max_length=20, null=True)
    state = models.CharField(max_length=20, null=True)
    city = models.CharField(max_length=20, null=True)
    street_address = models.CharField(max_length=50, null=True)
    postcode = models.IntegerField(null=True)
    phone_number = models.IntegerField(null=True)
    gender = models.CharField(choices=(('Male', 'Male'), ('Female', 'Female')), max_length=10, null=True)
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


def one_week_hence():
    return timezone.now() + timezone.timedelta(days=7)


class Admin(models.Model):
    ordered_product = models.ForeignKey(Product, on_delete=models.CASCADE, related_name='admin')
    customer = models.ForeignKey(User, on_delete=models.CASCADE)
    status = models.IntegerField(choices=order_status, default=0)
    order_placed_date = models.DateTimeField(default=timezone.now, blank=True, null=True)
    order_confirmed_date = models.DateTimeField(blank=True, null=True)
    packing_date = models.DateTimeField(blank=True, null=True)
    shipped_date = models.DateTimeField(blank=True, null=True)
    out_for_delivery_date = models.DateTimeField(blank=True, null=True)
    delivered_date = models.DateTimeField(default=one_week_hence, blank=True, null=True)
    order_cancelled_date = models.DateTimeField(blank=True, null=True)
    return_request_placed_date = models.DateTimeField(blank=True, null=True)
    return_request_acknowledged_date = models.DateTimeField(blank=True, null=True)
    courier_service_informed_date = models.DateTimeField(blank=True, null=True)
    return_product_verified_date = models.DateTimeField(blank=True, null=True)
    refund_completed_date = models.DateTimeField(blank=True, null=True)
    delivered = models.BooleanField(default=False)

    def __str__(self):
        return '%s ==> %s ==> %s' % (self.customer.username, self.ordered_product.title, self.get_status_display())


notification_status = [(0, 'Your Order is Placed'),
                       (1, 'Your Order is Confirmed'),
                       (2, 'Order Packed'),
                       (3, 'Your product is Shipped'),
                       (4, 'Your product is out for Delivery'),
                       (5, 'Your product is successfully Delivered'),
                       (6, 'Your order is Cancelled'),
                       (7, 'Your Return Request is Placed'),
                       (8, 'Your Return Request is Acknowledged'),
                       (9, 'Courier Service near you is Informed'),
                       (10, 'Return Product Verified'),
                       (11, 'Refund Completed')
                       ]


class Notification(models.Model):
    user = models.ForeignKey(User, on_delete=models.CASCADE)
    order = models.ForeignKey(Admin, on_delete=models.CASCADE)
    text = models.IntegerField(choices=notification_status, default=0)
    seen = models.BooleanField(default=False)
    close = models.BooleanField(default=False)

    def __str__(self):
        return '%s ==> %s' % (self.user.username, self.order.ordered_product.title)
