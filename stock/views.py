from django.shortcuts import render
from django.core.urlresolvers import reverse_lazy
from django.views.generic import ListView, CreateView, DetailView, FormView, TemplateView
from django.views.generic.dates import MonthArchiveView
from django.db.models import F
from django.http import HttpResponseRedirect

from datetime import datetime, timedelta, date

# Create your views here.
from .models import StockRec
from buy.models import BuyItem
from .forms import DateRangeForm


def BuyStockIn(request):
	if request.method == 'POST':
		in_list = request.POST
		print(in_list)
		for key, val in in_list.items():
			is_end = in_list.get(key+'end', None)
			if not key.isdigit():
				continue
			try:
				item = BuyItem.objects.get(pk=int(key))
			except BuyItem.DoesNotExist:
				continue
			else:
				item.end = True if is_end=='on' else False
				if is_end=='on':
					print(is_end)
				item.save()
				amount= val
				if amount.isdigit():
					StockRec.objects.create(buyitem=item, amount=int(amount))
					
	return HttpResponseRedirect(reverse_lazy('stock:showincomplete'))






def ShowIncompletes(request):
	form = DateRangeForm(request.POST or None)
	if request.method == 'POST':
		if form.is_valid():
			start = form.cleaned_data['start']
			end = form.cleaned_data['end']
	else:
		end = date.today()
		start = end - timedelta(30)
		
	query_set = BuyItem.objects.filter(buy__date__range=(start, end)).filter(end=False, buy__commiter__isnull=False).order_by('drug__firm','drug__name')
	object_list = filter(lambda item: not item.is_completed, query_set)
	return render(request, 'stock/미입고내역.html', {'object_list':object_list, 'form':form})




class StockInMTV(TemplateView):
	template_name = 'stock/stockin_month.html'


class StockInMAV(MonthArchiveView):
	model = StockRec
	date_field = 'date'
	make_object_list = True


	def get_context_data(self, **kwargs):
		context = super(StockInMAV, self).get_context_data(**kwargs)
		query_set = self.get_queryset().filter(amount__gt=0)
		total_price = 0
		for s in query_set:
			total_price+=s.total_price
		context['total_price'] = total_price
		context['object_list'] = query_set
		return context





























