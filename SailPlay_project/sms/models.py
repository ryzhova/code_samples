from django.db import models


class SMSLog(models.Model):

    status = models.CharField(max_length=30, default='sent')
    handler = models.CharField(max_length=50)
    phone = models.CharField(max_length=11)
    msg = models.CharField(max_length=255)
    error_code = models.IntegerField(null=True)
    error_msg = models.CharField(max_length=255, null=True)
