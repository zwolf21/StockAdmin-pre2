from django import forms


class XlFileForm(forms.Form):
	xlfile = forms.FileField()
	recreate = forms.BooleanField(label='기존 데이터 삭제 후 다시 만들기', required=False)