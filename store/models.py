from django.db import models
import datetime
from django.contrib.auth.models import User
from django.db.models.signals import post_save 
# Create your models here.


#creating for customer profile
class Profile(models.Model):
    user = models.OneToOneField(User, on_delete=models.CASCADE) #delete profile and stuff
    date_modified = models.DateTimeField(User,auto_now=True)
    phone = models.CharField(blank=True)
    address1 = models.CharField(blank=True,max_length=200)
    address2 = models.CharField(blank=True,max_length=200)
    state = models.CharField(blank=True,max_length=200)
    city = models.CharField(max_length=100,blank=True)
    zipcode = models.CharField(blank=True,max_length=200)
    country = models.CharField(blank=True,max_length=200)
    old_cart = models.CharField(blank=True,max_length=200,null=True)
   

    def __str__(self):
        # return super().__str__()
        return self.user.username
    
def create_profile(sender,instance,created, **kwargs):
    if created:
        user_profile = Profile(user=instance)
        user_profile.save()

post_save.connect(create_profile, sender=User)  #automate profile

#categories of product 
class Category(models.Model):
    name = models.CharField(max_length=254)
    def __str__(self):
        return self.name

#customers details
class Customer(models.Model):
    first_name = models.CharField(max_length=254)
    last_name = models.CharField(max_length=254)
    phone = models.CharField(max_length=10)
    email = models.EmailField(max_length=254)
    password = models.CharField(max_length=254)

    def __str__(self):
        return f'{self.first_name} {self.last_name}'
    
 #product details 
class Product(models.Model): 
    name = models.CharField(max_length=254)
    price = models.DecimalField(max_digits=6,default=0,decimal_places=2)
    category = models.ForeignKey(Category, on_delete=models.CASCADE, default=1)
    description = models.CharField(max_length=254,null=True,blank=True,default='')

    #adding sales 
    is_sale = models.BooleanField(default=False)
    sale_price = models.DecimalField(max_digits=6,default=0,decimal_places=2)

    image = models.ImageField(upload_to='uploads/product')
    def __str__(self):
        return self.name
    
#Customers orders 
class Order(models.Model):
    product = models.ForeignKey(Product,on_delete=models.CASCADE)
    customer = models.ForeignKey(Customer,on_delete=models.CASCADE)
    quantity =models.ImageField(default=1)
    address = models.CharField(max_length=200, default="",blank=True)
    phone = models.CharField(max_length=10,default='',blank=True)
    date = models.DateField(default=datetime.datetime.today)
    status = models.BooleanField(default=False)

    def __str__(self):
        return self.product