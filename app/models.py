from django.db import models
from django.contrib.auth.models import User
import os
from django.conf import settings
from django.core.validators import MaxValueValidator, MinValueValidator
from django.utils.timezone import now
from datetime import timedelta


class UserProfile(models.Model):
    user = models.OneToOneField(User, on_delete=models.CASCADE)
    phone = models.CharField(max_length=15)
    address = models.CharField(max_length=100)
    profile_pic = models.ImageField(upload_to='profile_pics/', blank=True)

    vendor = models.BooleanField(default=False)

    rating = models.DecimalField(max_digits=2, decimal_places=1, default=0)
    no_of_sales = models.PositiveIntegerField(default=0)
    products_uploaded = models.PositiveIntegerField(default=0, validators=[MaxValueValidator(99999)])
    total_sales = models.DecimalField(max_digits=10, decimal_places=2, default=0)

    # def update_max_uploads(self):
    #     """Adjust max_uploads based on the user's rating."""
    #     if self.rating >= 4.5:  # Top-tier users
    #         self.max_uploads = 20
    #     elif self.rating >= 4.0:
    #         self.max_uploads = 15
    #     elif self.rating >= 3.5:
    #         self.max_uploads = 10
    #     else:
    #         self.max_uploads = 5
    #     self.save()

    # def can_upload(self):
    #     """Check if the user can upload more items."""
    #     return self.uploads < self.max_uploads

    # def __str__(self):
    #     return f"{self.user.username} '''- Max Uploads: {self.max_uploads}''' - Rating: {self.rating}"

    def __str__(self):
        return f"{self.user.username} "

class Category(models.Model):
    category_name = models.CharField(max_length=100, unique=True)

    def __str__(self):
        return self.category_name

class Product(models.Model):

    category = models.ForeignKey(Category, on_delete=models.SET_NULL, null=True, blank=True)

    product_name = models.CharField(max_length=200)
    product_description = models.TextField()
    product_price = models.DecimalField(max_digits=8, decimal_places=2)
    RATING_CHOICES = [
        (1, 'New'),
        (2, 'Excelent'),
        (3, 'Good'),
        (4, 'Fair'),
        (5, 'Poor'),
    ]
    product_rating = models.IntegerField(choices=RATING_CHOICES, default=1)
    
    stock = models.PositiveIntegerField(default=1)
    created_at = models.DateTimeField(auto_now_add=True)
    created_by = models.ForeignKey(User, on_delete=models.SET_NULL, null=True, blank=True)
    
    def __str__(self):
        return self.product_name

class ProductImage(models.Model):
    product = models.ForeignKey(Product, on_delete=models.CASCADE,related_name='product_image')
    image = models.ImageField(upload_to='products/')

    def delete(self, *args, **kwargs):
        # Delete the image file from the filesystem
        if self.image:
            image_path = os.path.join(settings.MEDIA_ROOT, self.image.name)
            if os.path.exists(image_path):
                os.remove(image_path)
        super().delete(*args, **kwargs)  # Call the parent class delete method

    def __str__(self):
        return f'{self.product.product_name}'

class Favorite(models.Model):
    user = models.ForeignKey(User, on_delete=models.CASCADE)  # Associate each product with a user
    product = models.ForeignKey(Product, on_delete=models.CASCADE)
    
    def __str__(self):
         return f"name : {self.user.username}"

class Cart(models.Model):
    user = models.ForeignKey(User, on_delete=models.CASCADE)
    product = models.ForeignKey(Product, on_delete=models.CASCADE)
    quantity = models.PositiveIntegerField(default=1)  # To store the quantity of products
    
    def __str__(self):
         return f"name : {self.user.username}"

class OrderedBy(models.Model):
    userprofile = models.ForeignKey(UserProfile, on_delete=models.CASCADE)
    address = models.CharField(max_length=100)
    date = models.DateTimeField(auto_now_add=True)
    process = models.BooleanField(default=0)
    total = models.DecimalField(max_digits=8, decimal_places=2)

    def can_cancel(self):
        time_difference = now() - self.date
        return time_difference <= timedelta(seconds=10)

    def __str__(self):
         return f"{self.userprofile.user.username} time:{self.date} "

class Ordered(models.Model):
    product = models.ForeignKey(Product, on_delete=models.CASCADE)
    quantity = models.PositiveIntegerField()
    orderedby = models.ForeignKey(OrderedBy,on_delete=models.CASCADE)

    def __str__(self):
         return f"{self.product.product_name}"

class EsewaTransaction(models.Model):
    user = models.ForeignKey(User, on_delete=models.CASCADE)
    amount = models.FloatField()
    status = models.CharField(max_length=10, choices=[('pending', 'Pending'), ('completed', 'Completed'), ('failed', 'Failed')])
    transaction_id = models.CharField(max_length=255, null=True, blank=True)
    created_at = models.DateTimeField(auto_now_add=True)

    def __str__(self):
        return f'Transaction for {self.user.username} - {self.amount}'

class Feedback(models.Model):
    userprofile = models.ForeignKey(UserProfile,on_delete=models.CASCADE)
    message = models.CharField(max_length=200)
    sent = models.DateTimeField(auto_now_add=True)

    def __str__(self):
        return f"{self.userprofile.user.email} at {self.sent}"