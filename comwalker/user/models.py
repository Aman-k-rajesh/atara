from django.db import models
from service.models import *
# Create your models here.
import os
from django.core.files.storage import default_storage

from django.db import models
import os
from django.conf import settings

class com_TB(models.Model):
    Image = models.ImageField(upload_to='profile_images/', null=True, blank=True)
    FullName = models.CharField(max_length=255)
    Email = models.EmailField()
    Password = models.CharField(max_length=255)
    Location = models.CharField(max_length=255)
    Address = models.CharField(max_length=255)
    PinAddress = models.CharField(max_length=10)

    def __str__(self):
        return self.FullName

    def get_image_url(self):
        """Return a default image if the file is missing"""
        if self.Image:
            image_path = os.path.join(settings.MEDIA_ROOT, str(self.Image))
            if os.path.exists(image_path):
                return self.Image.url
        return "/media/user/default.jpg"


    def save(self, *args, **kwargs):
        # Delete old image if new image is being uploaded
        try:
            old_instance = com_TB.objects.get(pk=self.pk)
            if old_instance.Image and old_instance.Image != self.Image:
                if os.path.isfile(old_instance.Image.path):
                    default_storage.delete(old_instance.Image.path)
        except com_TB.DoesNotExist:
            pass
        super().save(*args, **kwargs)




# class book_TB(models.Model):
#     ProductName=models.CharField(max_length=450)
#     Price=models.CharField(max_length=250)
#     ServiceCentreName=models.CharField(max_length=450)
#     Quantity=models.CharField(max_length=50)
#     AddAddress=models.CharField(max_length=1000)
#     sp=models.ForeignKey(padd_DB,on_delete=models.CASCADE,null=True)
#     Services=models.ForeignKey(Service_DB,on_delete=models.CASCADE,null=True)
#     uf=models.ForeignKey(com_TB,on_delete=models.CASCADE,null=True)
#     Paymentstatus=models.BooleanField(default='False')
#     Bookingstatus=models.BooleanField(default='False')
#     def __str__(self):
#         return self.ProductName


class book_TB(models.Model):
    ProductName=models.CharField(max_length=450)
    Price=models.CharField(max_length=250)
    ServiceCentreName=models.CharField(max_length=450)
    Quantity=models.CharField(max_length=50)
    AddAddress=models.CharField(max_length=1000)
    sp=models.ForeignKey(padd_DB,on_delete=models.CASCADE,null=True)
    Services=models.ForeignKey(Service_DB,on_delete=models.CASCADE,null=True)
    uf=models.ForeignKey(com_TB,on_delete=models.CASCADE,null=True)
    Paymentstatus = models.BooleanField(default=False)
    Bookingstatus = models.BooleanField(default=False)

    source = models.CharField(
        max_length=50,
        choices=[('database', 'Database'), ('dataset', 'Dataset')],
        default='database'  # Default to database if not specified
    )  # New field

    def __str__(self):
        return self.ProductName



class User_Feedback(models.Model):
    Name=models.CharField(max_length=250)
    Email=models.EmailField(max_length=450)
    Feedback=models.CharField(max_length=1000)
    user=models.ForeignKey(com_TB,on_delete=models.CASCADE)
    def __str__(self):
        return self.Name
    







# user/models.py
from django.db import models
from django.contrib.auth.models import User
from service.models import padd_DB
from .models import com_TB


class Review(models.Model):
    product = models.ForeignKey(padd_DB, on_delete=models.CASCADE, blank=True, null=True)
    user = models.ForeignKey(User, on_delete=models.CASCADE, blank=True, null=True)
    uname = models.CharField(max_length=150, blank=True, null=True)
    pname = models.CharField(max_length=150, blank=True, null=True)
    rating = models.IntegerField()
    comment = models.TextField()
    image = models.ImageField(upload_to='review_images/', blank=True, null=True)
    video = models.FileField(upload_to='review_videos/', blank=True, null=True)
    created_at = models.DateTimeField(auto_now_add=True)

    def __str__(self):
        return f"{self.uname} - {self.pname} - {self.rating}⭐"

from django.db import models
from django.contrib.auth.models import User

class CommunityPost(models.Model):
    user = models.ForeignKey(User, on_delete=models.CASCADE)
    product_name = models.CharField(max_length=100)
    description = models.TextField()
    image = models.ImageField(upload_to='community_posts/', blank=True, null=True)
    created_at = models.DateTimeField(auto_now_add=True)

    def __str__(self):
        return self.product_name
