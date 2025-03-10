from django.db import models

# Create your models here.
class prjctadm_DB(models.Model):
    Name=models.CharField(max_length=250)
    Email=models.EmailField(max_length=450)
    Password=models.CharField(max_length=50)

    def __str__(self):
        return self.Name
from django.db import models
