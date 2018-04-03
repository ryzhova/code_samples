import urllib.request
#import json

#from django.shortcuts import render
from django.http import HttpResponse
#from django.contrib import messages
#from django.urls import reverse

from .forms import SMSForm
from .sms_handler import get_handler, GATE_ERROR

url = 'http://127.0.0.1:8000/gate'

def index(request):

    if request.method == 'GET':

        print(request.META['QUERY_STRING'])
        qs = request.META['QUERY_STRING']
        url2 = url + "?" + qs



        #request = {'phone': 1111, 'msg': "ffffff"}

        try:
            #x = json.dumps(request).encode('utf-8')

            req = urllib.request.Request(url2)
            response = urllib.request.urlopen(req).read()
            #response = self.send_request(x)
            #response = json.loads(response.decode('utf-8'))
        except Exception:
            response = {'status': 'error', 'phone': 444444,
                        'error_code': "rrrrr", 'error_msg': 'Gate error'}
        return HttpResponse(response, content_type="application/json")
