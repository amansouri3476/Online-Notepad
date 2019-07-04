from django.db import models
from django.contrib.auth.models import User


# Create your models here.
class Note(models.Model):
    name = models.CharField(max_length=256)
    folder_name = models.CharField(max_length=256)
    data = models.TextField()
    user = models.ForeignKey(User, on_delete=models.CASCADE)
    y_r = models.IntegerField()
    m_r = models.IntegerField()
    d_r = models.IntegerField()
    h_r = models.IntegerField()
    min_r = models.IntegerField()
    s_r = models.IntegerField()
    y_m = models.IntegerField()
    m_m = models.IntegerField()
    d_m = models.IntegerField()
    h_m = models.IntegerField()
    min_m = models.IntegerField()
    s_m = models.IntegerField()


class Folder(models.Model):
    name = models.CharField(max_length=256)
    list_notes = models.TextField()
    user = models.ForeignKey(User, on_delete=models.CASCADE)
