from django.db import models
from django.contrib.auth.models import AbstractUser

class UserProfile(AbstractUser):
    phone = models.CharField(max_length=15, blank=True, null=True)
    preferred_payment_method = models.CharField(
        max_length=50,  # Adjust the max length as needed
        default='Card',  # Set a default value
        null=True,  # Allow null values if necessary
        blank=True,  # Allow blank values if necessary
    )

    # Override the related_name for groups and user_permissions to avoid conflicts
    groups = models.ManyToManyField(
        'auth.Group',
        related_name='userprofile_set',
        blank=True, null=True
    )
    user_permissions = models.ManyToManyField(
        'auth.Permission',
        related_name='userprofile_set',
        blank=True, null=True
    )

    def __str__(self):
        return f"{self.username} - {self.email}"


class Book_Table(models.Model):
    name=models.CharField(max_length=55)
    number=models.IntegerField()
    email=models.EmailField()
    date=models.DateField()

    def __str__(self):
        return self.name
    
class ItemList(models.Model):
    Category_name=models.CharField(max_length=15)

    def __str__(self):
        return self.Category_name

class Item(models.Model):
    Item_name=models.CharField(max_length=15)
    description=models.TextField(blank=False)
    Price=models.IntegerField()
    Category=models.ForeignKey(ItemList,related_name='name',on_delete=models.CASCADE)
    Image=models.ImageField(upload_to='items/')

    def __str__(self):
        return self.Item_name

class Tables(models.Model):
    name=models.CharField(max_length=55,null=True)
    number=models.CharField(max_length=55, null=True)
    email=models.EmailField(null=True, default='None')
    time=models.TimeField(null=True)
    preference=models.CharField(max_length=15, default='no_preference',null=True)
    occasion=models.CharField(max_length=15, default='None',null=True)
    special_requests = models.TextField(blank=True, null=True, default='None')
    person=models.IntegerField(null=True)
    date=models.DateField(null=True)
    status=models.CharField(max_length=15, default='None')

    def __str__(self):
        return self.name

class Orders(models.Model):
    item = models.ForeignKey(Item, on_delete=models.CASCADE)
    quantity = models.IntegerField()
    total_price = models.DecimalField(max_digits=10, decimal_places=2)

    def __str__(self):
        return f"Order of {self.item.Item_name} x {self.quantity}"

class p_orders(models.Model):
    ORDER_STATUS_CHOICES = [
        ('pending', ('Pending')),
        ('shipped', ('Shipped')),
        ('delivered', ('Delivered')),
        ('canceled', ('Canceled')),
    ]

    user = models.ForeignKey(UserProfile, on_delete=models.CASCADE)
    item = models.ForeignKey(Item, on_delete=models.CASCADE)
    quantity = models.IntegerField()
    total_price = models.DecimalField(max_digits=10, decimal_places=2)
    order_status = models.CharField(max_length=10, choices=ORDER_STATUS_CHOICES, default='pending')

    def __str__(self):
        return f"Order of {self.item.Item_name} x {self.quantity} - Status: {self.get_order_status_display()}"
