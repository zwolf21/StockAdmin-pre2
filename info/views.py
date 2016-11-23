from django.shortcuts import render, render_to_response
from django.core.urlresolvers import reverse_lazy
from django.views.generic.edit import FormView
from django.views.generic import ListView, DetailView, CreateView, TemplateView
from django.conf import settings
from django.db.models import Q

import os, sys

from .models import Info

from .forms import XlFileForm
from .modules.utils import xlDB2DicIter, is_xlfile


from django.utils import simplejson
from django.http import HttpResponse



# Create your views here.

class DrugInfoFromXlFile(FormView):
	form_class = XlFileForm
	template_name = 'info/get_xlfile_form.html'

	def form_valid(self, form):
		recreate = form.cleaned_data['recreate']
		xlfile = self.request.FILES['xlfile']

		if not is_xlfile(xlfile.name):
			context = {
				'error_message': '파일 형식이 일치하지 않습니다',
				'file_name' : xlfile.name
			}
			return render_to_response('info/update_failure.html', context)

		temp_file = os.path.join(settings.MEDIA_ROOT,'temp.xls')
		with open(temp_file, 'wb') as fp:
			fp.write(xlfile.read())
		di_table = xlDB2DicIter(temp_file)
		os.remove(temp_file)

		src_field_set = set(di_table[0])
		essential_field_set = {'약품코드','EDI코드','약품명(한글)','제약회사명','일반단가','수가명','규격단위'}
		if not essential_field_set < src_field_set:
			context = {
				'error_message' : '엑셀파일에 지정된 필수 컬럼(열) 항목이 없습니다',
				'essential_fields' : essential_field_set,
				'missing_fields' : essential_field_set - src_field_set,
				'input_file_fields': src_field_set,
				'file_name' : xlfile.name
				}
			return render_to_response('info/update_failure.html', context)

		if recreate:
			Info.objects.all().delete()

		context = {
			'success_count' : 0,
			'failure_count' : 0,
			'failures' : [],
			'why' : ''
		}
		success_count = 0
		for row in di_table:
			try:
				Info.objects.create(
					edi = int(row['EDI코드']),
					code = row['약품코드'],
					name = row['약품명(한글)'],
					name_as = row['수가명'],
					firm = row['제약회사명'],
					price = row['일반단가'],
					pkg_amount = row.get('포장단위') or 1,
					standard_unit = row['규격단위'],
					narcotic_class = int(row.get('약품법적구분') or 0)
				)
			except:
				exception = {}
				type_err, val_err, trcbk = sys.exc_info()
				context['failures'].append({
					'error_type': type_err.__name__,
					'error_value': val_err,
					'error_drug_name': row.get('약품명(한글)','약품명 미지정'),
					'error_drug_code': row.get('약품코드','약품코드 미지정')
					})
				context['failure_count']+=1
			else:
				context['success_count']+=1
		context['total_count'] = context['failure_count']+context['success_count']
		return render_to_response('info/update_result.html', context)

class IndexTV(TemplateView):
	template_name = "info/drug_info.html"

