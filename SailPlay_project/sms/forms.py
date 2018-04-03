from django import forms


class SMSForm(forms.Form):

    HANDLER_CHOICES = (
        ('SMSC', 'СМС-Центр'),
        ('SMSTRAFFIC', 'СМС-Трафик'),
        ('TEST', 'Тест'),
    )

    handler = forms.ChoiceField(choices=HANDLER_CHOICES)
    phone = forms.CharField(max_length=11)
    msg = forms.CharField(max_length=255)
