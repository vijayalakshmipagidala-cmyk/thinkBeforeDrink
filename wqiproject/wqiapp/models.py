from django.db import models

from django.contrib.auth.models import User
# Create your models here.
class signUpVals(models.Model):
    signUpName=models.CharField();
    signUpEmail=models.EmailField()
    signUpPass=models.CharField()


class WaterData(models.Model):
    user = models.ForeignKey(User, on_delete=models.CASCADE)
    ph = models.FloatField()
    tds = models.FloatField()
    hardness = models.FloatField()
    turbidity = models.FloatField()
    conductivity = models.FloatField(null=True, blank=True)
    wqi=models.FloatField()
    created = models.DateTimeField(auto_now_add=True)

    def __str__(self):
        return f"{self.user.username} - {self.ph}"
