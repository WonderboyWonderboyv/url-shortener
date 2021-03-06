from django.http import HttpResponseRedirect
from django.conf import settings
DEFAULT_REDIRECT_URL = getattr(settings, "DEFAULT_REDIRECT_URL", "http://www.inbits.com:8000")
def wildcard_redirect(request, path=None):
	url = DEFAULT_REDIRECT_URL
	if path is not None:
		url = DEFAULT_REDIRECT_URL + "/" + path
	return HttpResponseRedirect(url)