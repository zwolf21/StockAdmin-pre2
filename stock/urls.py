from django.conf.urls import url, patterns

from .views import *
urlpatterns = patterns('',
	url(r'^stockin/$', BuyStockIn, name='stockin'),
	url(r'^showincompletes/$', ShowIncompletes, name='showincomplete'),

	url(r'^showMonth/$', StockInMTV.as_view(), name='show_month'),
	url(r'^showMonth/(?P<year>\d{4})/(?P<month>[a-z]{3})/$', StockInMAV.as_view(), name='stockin_month_archive'),


	url(r'^showPeriod/', stockin_plv, name='stockin_period'),

)
