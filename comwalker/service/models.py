from django.db import models

# Create your models here.
class Service_DB(models.Model):
    CentreName=models.CharField(max_length=250)
    Email=models.EmailField(max_length=450)
    Location=models.CharField(max_length=350)
    Address=models.CharField(max_length=350)
    PinAddress=models.CharField(max_length=350)
    CentreImage=models.ImageField(upload_to='servicereg')
    Password=models.CharField(max_length=50)
    approve = models.BooleanField(default=False)

    def __str__(self):
        return self.CentreName

class padd_DB(models.Model):
    Productimage=models.ImageField(upload_to='service')
    Name=models.CharField(max_length=250)
    Colour=models.CharField(max_length=350)
    Memorycapacity=models.CharField(max_length=250)
    Description=models.CharField(max_length=750)
    Price=models.CharField(max_length=250)
    Details=models.CharField(max_length=1000)
    # Review=models.CharField(max_length=750)
    Services=models.ForeignKey(Service_DB,on_delete=models.CASCADE,)

    def __str__(self):
        return self.Name




