from django import forms
from .models import StockRec
from django.utils.timezone import now
from django.db import models

from datetime import date, timedelta




class DateRangeForm(forms.Form):
	start = forms.DateField(label='시작일자', initial=date.today()-timedelta(7), widget = forms.TextInput(attrs={'readonly':'readonly', 'class':'form-control  input-sm'}))
	end = forms.DateField(label='종료일자', initial=date.today(), widget = forms.TextInput(attrs={'readonly':'readonly','class':'form-control  input-sm'}))
	indate = forms.DateField(label='입고일자', initial=date.today(), widget = forms.TextInput(attrs={'readonly':'readonly','class':'form-control  input-sm'}))

	general = forms.BooleanField(label='일반', initial=True, widget=forms.CheckboxInput(attrs={'class':'badgebox'}))
	narcotic = forms.BooleanField(label='마약', initial=True, widget=forms.CheckboxInput(attrs={'class':'badgebox'}))
	psychotic = forms.BooleanField(label='향정', initial=True, widget=forms.CheckboxInput(attrs={'class':'badgebox'}))


class StockRecAmountForm(forms.ModelForm):
	amount = forms.IntegerField(label='수량')

	class Meta:
		model = StockRec
		fields = ['amount']