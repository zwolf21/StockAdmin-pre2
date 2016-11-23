from ..models import Buy, BuyItem
from itertools import groupby
from datetime import datetime

# 발주생성, 제약사별 그룹핑
def create_buy(date=datetime.now()):
	incart = BuyItem.objects.filter(buy__isnull=True).order_by('drug__account')
	for g, items in groupby(incart, lambda x:x.drug.account):
		buy = Buy.objects.create(date=date)
		for item in items:
			buy.buyitem_set.add(item)
	return buy




