from django.db import models
from django.db.models import Sum, Max, Q
from django.contrib.auth.models import User
# Create your models here.


class Account(models.Model):
	name = models.CharField('도매상명', unique=True, max_length=50)
	tel = models.CharField('전화', max_length=50, null=True)
	fax = models.CharField('팩스', max_length=50, null=True, blank=True)
	email = models.EmailField('담당자 E-mail', null=True, blank=True)
	address = models.CharField('위치', max_length=100, null=True, blank=True)

	class Meta:
		verbose_name='도매상'
		verbose_name_plural='도매상'

	def __str__(self):
		return self.name




class Info(models.Model):

	def __str__(self):
		return self.name

	class Meta:
		verbose_name='약품정보'
		verbose_name_plural='약품정보'
		ordering = ['name_as']

	edi = models.IntegerField('EDI 코드', primary_key=True, editable=False)
	name = models.CharField('약품명', max_length=100)
	name_as = models.CharField('약품거래명', max_length=100, null=True)
	code = models.CharField('약품코드', max_length=20, null=True, editable=False)
	firm = models.CharField('제약회사명', max_length=50, null=True)
	price = models.PositiveIntegerField('단가', default=0)
	pkg_amount = models.PositiveIntegerField('포장수량', default=1, blank=True)
	purchase_standard = models.CharField('구매규격', max_length=50, null=True, blank=True)
	standard_unit = models.CharField('규격단위', max_length=50, null=True)
	narcotic_class = models.IntegerField('마약류구분', choices=[(0,'일반'),(1,'마약'),(2,'향정')], default=1)
	account = models.ForeignKey(Account, null=True, default=1, verbose_name='도매상')
	base_amount = models.IntegerField('기초재고', default=0)
	create_date = models.DateTimeField('생성시간', auto_now_add=True)
	modify_date = models.DateTimeField('수정시간', auto_now=True)
	by = models.ForeignKey(User, default=1, verbose_name='정보생성인')


	@property
	def current_stock(self):
		dynamic_amount = self.stockrec_set.filter(frozen=False).aggregate(Sum('amount'))['amount__sum'] or 0
		return dynamic_amount + self.base_amount

	@property
	def total_incomplete_amount(self):
		incomplete = 0
		for item in self.buyitem_set.filter(buy__isnull=False):
			incomplete += item.incomplete_amount
		return incomplete

	@property
	def total_stockin_amount(self):
		return self.stockrec_set.aggregate(Sum('amount'))['amount__sum'] or 0


	@property
	def last_stockin_date(self):
		return self.stockrec_set.aggregate(Max('date'))['date__max']

	@property
	def last_stockin_amount(self):
		if self.last_stockin_date:
			return self.stockrec_set.get(date=self.last_stockin_date).amount

	@property
	def last_buy_date(self):
		return self.buyitem_set.aggregate(Max('buy__date'))['buy__date__max']

	@property
	def last_buy_amount(self):
		if last_buy_date:
			return self.buyitem_set.get(date=last_buy_date).amount


