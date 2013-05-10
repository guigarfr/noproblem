from django.db import models
from noproblem.accounts.models import UserProfile

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
    def get_children(self):
    	return Problem.objects.filter(requirements=self).all()
    def degree_out(self):
    	return self.get_children().count()
	def data(self):
		"Returns the data needed to solve a problem"
        from noproblem.problems.pyconnecta import probs
        return getattr(probs, self.datos)()
    def solve(self,data):
        "Returns the data needed to solve a problem"
        from noproblem.problems.pyconnecta import probs
        return getattr(probs, self.solucion)(data)

class Solves(models.Model):
    user = models.ForeignKey(UserProfile)
    prob = models.ForeignKey(Problem)
    date = models.DateTimeField()
    time = models.TimeField()
    is_correct = models.BooleanField()




