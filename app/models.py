from django.db import models

# Create your models here.

#user data model
class User(models.Model):
    user_email = models.EmailField(max_length = 254)
    created_at = models.DateTimeField(auto_now_add=True)

    REQUIRED_FIELD = ['user_email', 'created_at']

    class Meta:
        app_label = 'app'
        db_table = 'user'
        verbose_name = 'User'
        verbose_name_plural = 'Users'


#auction product details
class Product(models.Model):
    user_id = models.ForeignKey(User, on_delete=models.CASCADE) 
    name = models.CharField(max_length=500)
    description = models.TextField()
    photo = models.CharField(max_length=256)
    minimum_bid = models.FloatField()
    bid_deadline = models.DateTimeField()
    created_at = models.DateTimeField(auto_now_add=True)
    updated_at = models.DateTimeField(auto_now=True)

    REQUIRED_FIELD = ["user_id", "name", "description", "photo", "minimum_bid", "bid_deadline", "created_at", "updated_at"]

    class Meta:
        app_label = 'app'
        db_table = 'product'
        verbose_name = 'Product'
        verbose_name_plural = 'Products'


# bid tables
class Bid(models.Model):
    product_id = models.ForeignKey(Product, on_delete=models.CASCADE) 
    bider = models.ForeignKey(User, on_delete=models.CASCADE)
    ask_price = models.FloatField()
    created_at = models.DateTimeField(auto_now_add=True)
    updated_at = models.DateTimeField(auto_now=True)

    
    REQUIRED_FIELD = ["product_id", "bider", "ask_price", "created_at", "updated_at"]

    class Meta:
        app_label = 'app'
        db_table = 'bid'
        verbose_name = 'Bid'
        verbose_name_plural = 'Bids'