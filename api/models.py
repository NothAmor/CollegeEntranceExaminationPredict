from django.db import models

# Create your models here.

# 一分一段
class FenDuan(models.Model):
    id = models.AutoField(primary_key=True)
    year = models.IntegerField()
    province = models.TextField()
    grade = models.IntegerField()
    section = models.TextField()
    sameGradePeopleCount = models.IntegerField()
    positionRecommendation = models.IntegerField()