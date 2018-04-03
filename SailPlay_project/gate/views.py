import json

from django.http import HttpResponse
from django.views.decorators.http import require_POST


#@require_POST
def gate(request):

    if request.method == "GET":
        try:
            limit = request.GET['limit']
        except KeyError:
            limit = 4
        try:
            offset = request.GET['offset']
        except KeyError:
            offset = 0
        print(limit, offset)
        answer = {'status': 'error', 'phone': 'ttttttt4444444',
                  'error_code': 1, 'error_msg': 'Wrong number'}
        binary_json = json.dumps(answer).encode('utf-8')
        return HttpResponse(binary_json, content_type="application/json")
