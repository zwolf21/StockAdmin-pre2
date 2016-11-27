from django.conf.urls import url, patterns

from .views import *
urlpatterns = patterns('',
	
	url(r'^showPeriod/$', StockInPTV.as_view(), name='show_period'),
	url(r'^showPeriod/result/list$', StockInPLV.as_view(), name='show_period_result_list'),
	url(r'^showPeriod/result/ano$', StockInPLVano.as_view(), name='show_period_result_ano'),

	url(r'^showIncomplete/$', StockIncompleteTV.as_view(), name='show_incomplete'),
	url(r'^showIncomplete/result/$', StockIncompleteLV.as_view(), name='show_incomplete_list'),
	url(r'^in/$', StockRecCV.as_view(), name='stockin')

)
