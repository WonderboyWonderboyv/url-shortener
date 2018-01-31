from __future__ import unicode_literals

from django.db import models
from shortener.models import ShortenUrl

class CountUrlManager(models.Manager):
	def create_event(self, instance):
		if isinstance(instance, ShortenUrl):
			obj, created = self.get_or_create(c_url=instance)
			obj.count +=1
			obj.save()
			return obj.count
		return None

class CountUrl(models.Model):
	c_url = models.OneToOneField(ShortenUrl)
	count = models.IntegerField(default=0)
	updated = models.DateTimeField(auto_now=True)
	timestamp = models.DateTimeField(auto_now_add=True)

	objects = CountUrlManager()

	def __str__(self):
		return "{i}".format(i=self.count)
	def __unicode__(self):
		return "{i}".format(i=self.count)
	
