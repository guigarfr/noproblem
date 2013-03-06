from django.db import models
from django.contrib.auth.models import User, UserManager

# Create your models here.
class Area (models.Model):
    name = models.CharField(max_length=100,unique=True)
    def __unicode__(self):
        return self.name

class SubArea (models.Model):
    name = models.CharField(max_length=100)
    area = models.ForeignKey(Area)
    def __unicode__(self):
        return u'%s (%s)' % (self.name, self.area.name)

class Problem (models.Model):
    category = models.ForeignKey(SubArea)
    title = models.CharField(max_length=200)
    wording = models.TextField()
    points = models.IntegerField()
    #crea_date = models.DateTimeField('fecha de creacion')
    created_at = models.DateTimeField(auto_now_add = True)
    updated_at = models.DateTimeField(auto_now = True)
    requirements = models.ManyToManyField('Problem',blank=True,null=True)
    datos = models.CharField(max_length=200)
    solucion = models.CharField(max_length=200)
    def __unicode__(self):
        return self.title


class CustomUser(User):
    # Use UserManager to get the create_user method, etc.
    objects = UserManager()
    # Our own fields
    credits = models.IntegerField()
    def __unicode__(self):
        return self.name


class Solves(models.Model):
    user = models.ForeignKey(CustomUser)
    prob = models.ForeignKey(Problem)
    date = models.DateTimeField()
    is_correct = models.BooleanField()




