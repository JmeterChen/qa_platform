from django.shortcuts import render
from django.http import Http404, HttpResponse
import datetime
# Create your views here.


def hours_ahead(request, offset):
	try:
		offset = int(offset)
	except ValueError:
		raise Http404()
	dt = datetime.datetime.now() + datetime.timedelta(hours=offset)
	html = f"In {offset} hour(s), it will be {str(dt).split('.')[0]}"
	return HttpResponse(html)


def get_year(request, year):
	return HttpResponse(f"Hello this Year is {year}！")


def test_extra(request, year):
	return HttpResponse(f"Hello this Year is {year}！")