import re
import http
import json
import csv
from django.shortcuts import render,redirect


from django.views.generic import TemplateView
from django.http import HttpResponse, JsonResponse, response
from netmiko import ConnectHandler
from pprint import pprint
from django.contrib import messages



class loginClass(TemplateView):
    def get(self,request):
        print("login get")
        return render(request,'loginpage.html')
    def post(self,request):
        print('login post')
        return render(request,'loginpage.html')