from django.db import models
from django.contrib.auth.models import User
from datetime import date

# Create your models here.
class UserProfile(models.Model):
    user = models.OneToOneField(User, on_delete=models.CASCADE)
    activation_key = models.CharField(max_length=255, blank=True)
    key_expires = models.DateTimeField(default=date.today)

    def __str__(self):
        return self.user.username

    class Meta:
        verbose_name_plural=u'Perfiles de Usuario'