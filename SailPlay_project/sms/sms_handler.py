import urllib.request
import json

from SailPlay_project.settings import SMS_HANDLERS
from .models import SMSLog

GATE_ERROR = 2


class SMSHandler():

    def send(self, phone, msg):
        request = {'phone': phone, 'msg': msg}

        try:
            response = self.send_request(json.dumps(request).encode('utf-8'))
            response = json.loads(response.decode('utf-8'))
        except Exception:
            response = {'status': 'error', 'phone': phone,
                        'error_code': GATE_ERROR, 'error_msg': 'Gate error'}

        log = SMSLog(status=response['status'], phone=phone, msg=msg,
                     handler=self.__class__.__name__)

        try:
            log.error_code = response['error_code']
            log.error_msg = response['error_msg']
        except KeyError:
            pass

        log.save()

        return response

    def send_request(self, data):
        raise NotImplementedError


class SMSC(SMSHandler):

    REALM = 'SMS'

    def __init__(self, url, login, password):
        self.url = url
        self.login = login
        self.password = password

    def send_request(self, data):

        auth_handler = urllib.request.HTTPBasicAuthHandler()
        auth_handler.add_password(realm=self.REALM, uri=self.url,
                                  user=self.login, passwd=self.password)
        opener = urllib.request.build_opener(auth_handler)

        req = urllib.request.Request(
            self.url, headers={"Content-type": "application/json"}, data=data
        )
        response = opener.open(req).read()
        return response


class SMSTraffic(SMSHandler):

    def __init__(self, url, token):
        self.url = url
        self.token = token

    def send_request(self, data):

        req = urllib.request.Request(
            self.url,
            headers={"Content-type": "application/json",
                     "X-AuthToken": self.token},
            data=data
        )
        response = urllib.request.urlopen(req).read()
        return response


class Test(SMSHandler):

    def __init__(self, url):
        self.url = url

    def send_request(self, data):

        req = urllib.request.Request(
            self.url, headers={"Content-type": "application/json"}, data=data
        )
        response = urllib.request.urlopen(req).read()
        return response


def get_handler(handler_name):

    if handler_name == 'SMSC':
        return SMSC(**SMS_HANDLERS[handler_name])

    elif handler_name == 'SMSTRAFFIC':
        return SMSTraffic(**SMS_HANDLERS[handler_name])

    elif handler_name == 'TEST':
        return Test(**SMS_HANDLERS[handler_name])

    else:
        raise ValueError
