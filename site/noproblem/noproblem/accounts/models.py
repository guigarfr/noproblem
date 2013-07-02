from django.db import models
from django.db.models import signals
from django.contrib.auth.models import User

# Create your models here.

class UserProfile(models.Model):
    # This field is required.
    user = models.OneToOneField(User, related_name='profile')

    # Other fields here
    credits = models.IntegerField(default=0)
    def __unicode__(self):
        return self.user.username
