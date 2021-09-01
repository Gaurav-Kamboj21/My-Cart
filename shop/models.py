from django.db import models
from django.utils import timezone
from django.contrib.auth.models import User
from .utils import email
from dirtyfields import DirtyFieldsMixin
# Create your models here.


class Users(models.Model):
    User_CHOICES = (
        ('Seller', 'Seller'),
        ('Customer', 'Customer')
    )
    user_name = models.CharField(max_length=50, default='')
    user_email = models.CharField(max_length=50, default='')
    user_type = models.CharField(max_length=20, choices=User_CHOICES, default='customer')
    user_address = models.TextField()
    user_state = models.CharField(max_length=50, default='India')
    user_city = models.CharField(max_length=50)
    user_Zip = models.CharField(max_length=10)
    user_phone = models.CharField(max_length=15, default='+91')
    user_password = models.CharField(max_length=50,default='')
    user_password2 = models.CharField(max_length=50,default='')

    def __str__(self):
        return self.user_name


class Products(models.Model):
    product_id = models.AutoField
    product_name = models.CharField(max_length=50)
    category = models.CharField(max_length=50, default="")
    subcategory = models.CharField(max_length=50, default="")
    price = models.IntegerField(default=0)
    desc = models.TextField(max_length=300, default='Best')
    pub_date = models.DateField(default=timezone.now)
    image = models.ImageField(upload_to='shop/images', default="")

    def __str__(self):
        return self.product_name


class Contact(models.Model):
    msg_id = models.AutoField(primary_key=True)
    name = models.CharField(max_length=50)
    email = models.CharField(max_length=70, default="")
    phone = models.CharField(max_length=70, default="")
    desc = models.CharField(max_length=500, default="")


    def __str__(self):
        return self.name


class Orders(models.Model):
    order_id = models.AutoField(primary_key=True)
    items_json = models.CharField(max_length=5000)
    name = models.CharField(max_length=90)
    email = models.CharField(max_length=70)
    address = models.CharField(max_length=70)
    city = models.CharField(max_length=70)
    state = models.CharField(max_length=70)
    zip_code = models.CharField(max_length=70)
    phone = models.CharField(max_length=70, default="")
    amount = models.IntegerField(default=0)

    def __str__(self):
        return self.name


class OrderUpdate(DirtyFieldsMixin, models.Model):
    update_id = models.AutoField(primary_key=True)
    order_id = models.IntegerField(default="")
    update_desc = models.CharField(max_length=5000)
    timestamp = models.DateTimeField(default=timezone.now)
    # info = models.ForeignKey(User, on_delete=models.CASCADE, default="")

    def save(self, *args, **kwargs):
        if self.is_dirty():
            dirty_fields = self.get_dirty_fields()
            if 'update_desc' in dirty_fields:
               email('csecec.gaurav1702635@gmail.com')
        super().save(*args, **kwargs)
