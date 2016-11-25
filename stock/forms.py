from django import forms
from .models import BuyItem, Buy
from django.utils.timezone import now
from django.db import models

from datetime import date, timedelta



class DateRangeForm(forms.Form):
	start = forms.DateField(label='시작일자', initial=date.today(), widget = forms.TextInput(attrs={'readonly':'readonly'}))
	end = forms.DateField(label='종료일자', initial=date.today(), widget = forms.TextInput(attrs={'readonly':'readonly'}))
	general = forms.BooleanField(label='일반', initial=True)
	narcotic = forms.BooleanField(label='마약', initial=True)

