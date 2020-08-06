from django.shortcuts import render
from django.http import Http404, HttpResponse
from django.views.decorators.csrf import csrf_exempt,csrf_protect
from django.utils.decorators import method_decorator
import json
import datetime
from django.views import View

# Create your views here.


@csrf_exempt
def hours_ahead(request, offset):
	try:
		offset = int(offset)
	except ValueError:
		raise Http404()
	dt = datetime.datetime.now() + datetime.timedelta(hours=offset)
	html = f"In {offset} hour(s), it will be {str(dt).split('.')[0]}"
	return HttpResponse(html)


@csrf_exempt
# @csrf_protect
def get_year(request, year):
	return HttpResponse(f"Hello this Year is {year}！")


def test_extra(request, year):
	return HttpResponse(f"Hello this Year is {year}！")


def user_list(request):
	userList = ["kobe", "chenBoLin"]
	return HttpResponse(json.dumps(userList))


# class StudentView(View):
#
# 	@method_decorator(csrf_exempt)
# 	def dispatch(self, request, *args, **kwargs):
# 		return super(StudentView, self).dispatch(request, *args, **kwargs)
#
# 	def get(self, requests, *args, **kwargs):
# 		return HttpResponse("GET")
#
# 	def post(self, requests, *args, **kwargs):
# 		return HttpResponse("POST")
#
# 	def put(self, requests, *args, **kwargs):
# 		return HttpResponse("PUT")
#
# 	def delete(self, requests, *args, **kwargs):
# 		return HttpResponse("DELETE")

@method_decorator(csrf_exempt, name='dispatch')
class StudentView(View):
	
	def get(self, requests, *args, **kwargs):
		return HttpResponse("GET")
	
	def post(self, requests, *args, **kwargs):
		return HttpResponse("POST")
	
	def put(self, requests, *args, **kwargs):
		return HttpResponse("PUT")
	
	def delete(self, requests, *args, **kwargs):
		return HttpResponse("DELETE")