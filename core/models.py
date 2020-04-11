from django.db import models
from django.conf import settings
from django.shortcuts import reverse


class Item(models.Model):
    LOCATIONS = [
        ("Location1", "Location1"),
        ("Location2", "Location2"),
    ]
    TYPES = [
        ("Flight", "Flight"),
        ("Ground", "Ground"),
    ]

    remarks = models.TextField(default='')
    added_ts = models.DateTimeField(auto_now_add=True)
    quantity = models.IntegerField(default=1)
    location = models.CharField(max_length=50, choices=LOCATIONS)
    item_type = models.CharField(max_length=50, choices=TYPES)
    item_name = models.CharField(max_length=255)
    model_num = models.CharField(max_length=255)
    project_name = models.CharField(max_length=255)
    item_serial_num = models.CharField(max_length=255)
    calibration_date = models.DateTimeField()
    slug = models.SlugField()

    def __str__(self):
        return self.item_name

    def get_absolute_url(self):
        return reverse("core:product", kwargs={
            'slug': self.slug
        })

    def get_add_to_cart_url(self):
        return reverse('core:add-to-cart', kwargs={
            'slug': self.slug
        })

    def get_remove_from_cart_url(self):
        return reverse('core:remove-from-cart', kwargs={
            'slug': self.slug
        })


class OrderItem(models.Model):
    user = models.ForeignKey(
            settings.AUTH_USER_MODEL,
            on_delete=models.CASCADE,
            blank=True,
            null=True
        )
    ordered = models.BooleanField(default=False)
    item = models.ForeignKey(Item, on_delete=models.CASCADE)
    quantity = models.IntegerField(default=1)
    
    def __str__(self):
        return "{} of {}".format(self.quantity,self.item.item_name)


class Order(models.Model):
    user = models.ForeignKey(
            settings.AUTH_USER_MODEL,
            on_delete=models.CASCADE
        )
    ordered = models.BooleanField(default=False)
    items = models.ManyToManyField(OrderItem)
    start_date = models.DateTimeField(auto_now_add=True)
    ordered_date = models.DateTimeField()
    

    def __str__(self):
        return self.user.username
