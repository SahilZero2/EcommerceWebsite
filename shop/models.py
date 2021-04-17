from django.db import models
from django.contrib.auth.models import User
# Create your models here.

class Customer(models.Model):
    user = models.OneToOneField(User,on_delete=models.CASCADE)
    name = models.CharField(max_length=200)
    email = models.CharField(max_length=200)

    def __str__(self):
        return self.name


class Products(models.Model):
    name = models.CharField(max_length=50)
    desc = models.CharField(max_length=300)
    price = models.FloatField(default='')
    thumbnail = models.ImageField(upload_to = 'profile_picture/')


    def __str__(self):
        return self.name


class Order(models.Model):
    customer = models.ForeignKey(Customer , on_delete=models.CASCADE)
    date_orderd = models.DateTimeField(auto_now_add=True)
    transection_id = models.CharField( max_length=200)

    def __str__(self):
        return str(self.id)

    @property
    def get_cart_total(self):
        orderitems = self.orderitem_set.all()
        total =sum([item.get_total for item in orderitems])
        return total

    @property
    def get_cart_items(self):
        orderitems = self.orderitem_set.all()
        total =sum([item.quantity for item in orderitems])
        return total



class OrderItem(models.Model):
    products = models.ForeignKey(Products, on_delete=models.CASCADE)
    order = models.ForeignKey(Order, on_delete=models.CASCADE)
    quantity =models.IntegerField(default=0)
    date_added = models.DateTimeField(auto_now_add=True)

    @property
    def get_total(self):
        total = self.products.price * self.quantity
        return total
    

class ShippingAddress(models.Model):
    customer = models.ForeignKey(Customer, on_delete=models.CASCADE)
    order = models.ForeignKey(Order, on_delete=models.CASCADE)
    address = models.CharField( max_length=400)
    city = models.CharField(max_length=200)
    state = models.CharField(max_length=200)
    pincode = models.IntegerField()
    date_added = models.DateTimeField(auto_now_add=True)

    def __str__(self):
        return self.address
    


