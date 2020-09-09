from django.shortcuts import render
from django.http import HttpResponse
import json
from mypro.common.func import ding_push
# Create your views here.


def bugly_data(request):
	# return HttpResponse("Hello world!")
	req_data = json.loads(request.body)
	return HttpResponse(ding_push(req_data))