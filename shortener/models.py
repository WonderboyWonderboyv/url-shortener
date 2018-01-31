from __future__ import unicode_literals

from django.db import models
from .utils import create_shortcode
from django.conf import settings
from .validators import validate_url
#from django.core.urlresolvers import reverse
from django_hosts.resolvers import reverse
# Create your models here.
SHORTCODE_MAX = getattr(settings, "SHORTCODE_MAX", 15)



class ShortenUrlManager(models.Manager):
	def all(self, *args, **kwargs):
		qs_original = super(ShortenUrlManager, self).all(*args, **kwargs)
		qs = qs_original.filter(active=True)
		return qs
	def refresh_shortcode(self, items=None):
		new_codes = 0
		qs = ShortenUrl.objects.filter(id__gte=1)
		if items is not None and isinstance(items, int):
			qs = qs.order_by('-id')[:items]
		for q in qs:
			q.shortcode = create_shortcode(q)
			print(q.shortcode)
			q.save()
			new_codes += 1
		return "New codes made: {i}".format(i=new_codes)

class ShortenUrl(models.Model):
	url = models.CharField(max_length=220, validators=[validate_url])
	shortcode = models.CharField(max_length=15, unique=True, blank=True)
	updated = models.DateTimeField(auto_now=True)
	timestamp = models.DateTimeField(auto_now_add=True)
	active = models.BooleanField(default=True)

	objects = ShortenUrlManager()

	def save(self, *args, **kwargs):
		if self.shortcode is None or self.shortcode == "":
			self.shortcode = create_shortcode(self)
		super(ShortenUrl, self).save(*args, **kwargs)
	def __str__(self):
		return str(self.url)
	def __unicode__(self):
		return str(self.url)
	def get_short_url(self):
		url_path = reverse("shortcode", kwargs={'shortcode':self.shortcode,}, host='www', scheme='https')
		return url_path