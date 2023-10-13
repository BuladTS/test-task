from django.db import models


# Create your models here.


class MenuLink(models.Model):
    title = models.CharField(max_length=255)
    slug = models.SlugField(max_length=255, unique=True)
    url = models.CharField(max_length=255)
    level = models.IntegerField()
    left_key = models.IntegerField()
    right_key = models.IntegerField()

    def __str__(self):
        return self.title



