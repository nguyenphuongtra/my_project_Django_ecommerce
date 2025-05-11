from django.db import models
from django.contrib.auth.models import AbstractUser
from django.utils.translation import gettext_lazy as _

class User(AbstractUser):
    phone_number = models.CharField(max_length=15, blank=True)
    address = models.TextField(blank=True)
    wishlist = models.ManyToManyField('shop.Product', related_name='wishlisted_by', blank=True)
    avatar = models.ImageField(upload_to='users/avatars/', blank=True, null=True)

    def __str__(self):
        return self.username

