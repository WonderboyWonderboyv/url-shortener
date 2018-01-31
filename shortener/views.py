from django.shortcuts import render, get_object_or_404
from django.views import View
from .models import ShortenUrl
from django.http import HttpResponse, HttpResponseRedirect
from .forms import SubmitUrlForm
from counts.models import CountUrl
# Create your views here.

class FeatureView(View):
	def get(self, request, *args, **kwargs):
		return render(request, 'shortener/features.html', {})

class ContactView(View):
	def get(self, request, *args, **kwargs):
		return render(request, 'shortener/contact.html', {})

class HomeView(View):
	def get(self, request, *args, **kwargs):
		form = SubmitUrlForm()
		context = {'form':form,}
		return render(request, 'shortener/home.html', context)

	def post(self, request, *args, **kwargs):
		form = SubmitUrlForm(request.POST)
		template = 'shortener/home.html'
		context = {'form':form,}
		if form.is_valid():
			print(form.cleaned_data)
			url = form.cleaned_data.get("url")
			obj, created = ShortenUrl.objects.get_or_create(url=url)
			context = {'object':obj}
			if created:
				template = 'shortener/success.html'
			else:
				template = 'shortener/already-exists.html'
		return render(request, template, context)


class ShortenUrlRedirect(View):
	def get(self, request, shortcode=None, *args, **kwargs):
		print(shortcode)
		obj = get_object_or_404(ShortenUrl, shortcode=shortcode)
		obj_url = obj.url
		print(CountUrl.objects.create_event(obj))
		return HttpResponseRedirect(obj_url)
