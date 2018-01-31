from django.core.validators import URLValidator
from django.core.exceptions import ValidationError

def validate_url(value):
	url_validator = URLValidator()
	value_1_invalid = False
	value_2_invalid = False
	try:
		url_validator(value)
	except:
		value_1_invalid = True
	value2 = "http://" +  value
	try:
		url_validator(value2)
	except:
		value_2_invalid = True
	if value_1_invalid == True and value_2_invalid == True:
		raise ValidationError('Invalid URL for this field.')
	return value