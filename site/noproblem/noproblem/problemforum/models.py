# -*- coding: utf-8 -*-
from noproblem.problems.models import Problem
from noproblem.accounts.models import UserProfile
from django.db import models
from django.db.models.signals import post_save


# Create your models here.
class Thread(models.Model):
	prob = models.ForeignKey(Problem)
	def num_posts(self):
		return self.post_set.count()
	def num_replies(self):
		if self.post_set.count() == 0:
			return 0
		return self.post_set.count() - 1
	def last_post(self):
		if self.post_set.count():
			return self.post_set.order_by("created")[0]
	def __unicode__(self):
		return u"Mensajes %s" % (self.prob.title)

#Señal para crear un thread cada vez que se cree un problema
def create_thread_for_problem(sender, instance, created, **kwargs):  
    if created:  
       Thread.objects.create(prob=instance)
post_save.connect(create_thread_for_problem, sender=Problem)


class Post(models.Model):
	created = models.DateTimeField(auto_now_add=True)
	creator = models.ForeignKey(UserProfile, blank=True, null=True)
	thread = models.ForeignKey(Thread)
	body = models.TextField(max_length=10000)
	previous = models.ForeignKey('self', blank=True, null=True)

	def __unicode__(self):
		return u"%s - %s" % (self.creator, self.thread)

	def short(self):
		return u"%s\n%s" % (self.creator, self.created.strftime("%b %d, %I:%M %p"))
	short.allow_tags = True
