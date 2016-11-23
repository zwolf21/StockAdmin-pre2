from django.shortcuts import render
from django.core.urlresolvers import reverse_lazy
from django.views.generic import ListView, CreateView, DetailView, FormView, UpdateView, TemplateView, DeleteView
from django.views.generic.dates import DayArchiveView, TodayArchiveView, YearArchiveView, MonthArchiveView, ArchiveIndexView
from django.db.models import F
from django.http import HttpResponseRedirect
from django.contrib.auth.decorators import permission_required, login_required
from django.contrib.admin.views.decorators import staff_member_required
from itertools import groupby, chain
from django.forms.models import modelform_factory

from .modules.dbwork import *
from .models import BuyItem, Buy
from info.models import Info
from .forms import CreateBuyForm, BuyItemAddForm
from stock.models import StockRec
# Create your views here.


from StockAdmin.views import LoginRequiredMixin, PermissionRequiredMixin, Staff_memberRequiredMixin

class TestTV(TemplateView):
	template_name = "buy/test.html"



class BuyLV(ListView):
	model = Buy



class BuyDV(DetailView):
	model = Buy


@login_required
def create_buy(request):
	if request.method == 'POST':
		form = CreateBuyForm(request.POST)
		if form.is_valid():
			date = form.cleaned_data['date']
			cart_list = BuyItem.objects.filter(buy__isnull=True).order_by('drug__account')
			for g, itr in groupby(cart_list, lambda x:x.drug.account):
				buy = Buy.objects.create(date=date)
				for item in itr:
					buy.buyitem_set.add(item)
			return HttpResponseRedirect(reverse_lazy('buy:buy_list'))



class CartLV(ListView):
	template_name = 'buy/cart_list.html'

	def get_queryset(self):
		return BuyItem.objects.filter(buy__isnull=True)


class CartItemCV(LoginRequiredMixin ,CreateView):
	# model = BuyItem
	fields = ['amount']
	form_class = BuyItemAddForm
	success_url = reverse_lazy('buy:cartitem_add')
	template_name = 'buy/cart_list.html'


	def get_context_data(self, **kwargs):
		context = super(CartItemCV, self).get_context_data(**kwargs)
		context['object_list'] = BuyItem.objects.filter(buy__isnull=True)
		context['create_buy_form'] = CreateBuyForm
		return context

	def form_valid(self, form):

		name = self.request.POST.get('name')
		context = self.get_context_data()

		if name == '':
			return HttpResponseRedirect(self.success_url)

		try:
			drug = Info.objects.get(name=name)
		except (KeyError, Info.DoesNotExist):
			context['error_message'] = '해당품목이 존재 하지 않습니다(%s)' % name 
			return self.render_to_response(context)			
		else:
			if context['object_list'].filter(drug=drug).exists():
				return HttpResponseRedirect(self.success_url)
			form.instance.drug = drug
			form.instance.by = self.request.user
			return super(CartItemCV, self).form_valid(form)



class BuyItemCV(CartItemCV):
	template_name = 'buy/buyitem_list.html'

	def get_success_url(self):
		return reverse_lazy('buy:buyitem_add', args=(self.kwargs['slug'],))

	def get_context_data(self, **kwargs):
		context = super(BuyItemCV, self).get_context_data(**kwargs)
		context['object_list'] = BuyItem.objects.filter(buy__slug=self.kwargs['slug'])
		return context

	def form_valid(self, form):
		form.instance.buy = Buy.objects.get(slug=self.kwargs.get('slug'))
		return super(BuyItemCV, self).form_valid(form)



class CartItemUV(LoginRequiredMixin ,UpdateView):
	model = BuyItem
	fields = ['amount']
	success_url = reverse_lazy('buy:cartitem_add')
	template_name = 'buy/cartitem_update_form.html'

	def get_context_data(self, **kwargs):
		context = super(CartItemUV, self).get_context_data(**kwargs)
		context['object_list'] = BuyItem.objects.filter(buy__isnull=True)
		return context



class BuyItemUV(LoginRequiredMixin ,UpdateView):
	model = BuyItem
	fields = ['amount']
	template_name = 'buy/buyitem_update_form.html'

	def get_success_url(self):
		return reverse_lazy('buy:buyitem_add', args=(self.kwargs['slug'], ))

	def get_context_data(self, **kwargs):
		context = super(BuyItemUV, self).get_context_data(**kwargs)
		context['object_list'] = BuyItem.objects.filter(buy__slug=self.kwargs['slug'])
		return context




class CartItemDelV(LoginRequiredMixin, DeleteView):
	model = BuyItem
	success_url = reverse_lazy('buy:cartitem_add')
	template_name = 'buy/buyitem_confirm_delete.html'


class BuyItemDelV(LoginRequiredMixin, DeleteView):
	model = BuyItem
	template_name = 'buy/buyitem_confirm_delete.html'

	def get_success_url(self):
		return reverse_lazy('buy:buyitem_add', args=(self.kwargs['slug'], ))




def buy_commit(request, slug):
	if request.method == 'GET':
		if request.user.is_staff or request.user.is_superuser:
			try:
				buy = Buy.objects.get(slug=slug, commiter__isnull=True)
			except Buy.DoesNotExist:
				return HttpResponseRedirect(reverse_lazy('buy:detail', args=(slug,)))
			else:
				buy.commiter = request.user
				buy.save()
	return HttpResponseRedirect(reverse_lazy('buy:buy_list'))


class NarcoticLV(ListView):
	model = BuyItem
	template_name = 'buy/etc/narcotic_buy.html'


	def get_context_data(self, **kwargs):
		context = super(NarcoticLV, self).get_context_data(**kwargs)
		query_set =  BuyItem.objects.filter(buy__slug=self.kwargs['slug'], drug__narcotic_class=1, buy__commiter__isnull=False)
		max_Nrow = 15
		if query_set.count() < max_Nrow:
			padding_list = [''] * (max_Nrow- query_set.count())
		context['object_list'] = query_set
		context['padding'] = padding_list
		return context
















