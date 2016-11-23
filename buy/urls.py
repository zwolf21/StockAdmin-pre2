from django.conf.urls import url, patterns
from .views import *

# urlpatterns = patterns('',
#   url(r'^test$', TestTV.as_view(), name='test'),

#   url(r'^$', BuyLV.as_view(), name='buylist'),
#   url(r'^(?P<slug>[-\d]+)$', BuyDV.as_view(), name='buydetail'),
#   url(r'^buyupdate/(?P<slug>[-\d]+)$', BuyUDV.as_view(), name='buyupdate'),


#   url(r'^cart/$', BuyItemLV.as_view(), name='cart'),

#   url(r'^buyitemadd/(?P<slug>[-\d]+)/$', BuyItemCV.as_view(), name='buyitemadd'),
#   url(r'^cartitemadd/$', BuyItemCV.as_view(), name='cartitemadd'),



#   url(r'^itemupdate/(?P<pk>\d+)$', BuyItemUV.as_view(), name='itemupdate'),
#   url(r'^buydelete/(?P<pk>\d+)$', BuyItemDelV.as_view(), name='delete'),

#   url(r'^create$', BuyCV.as_view(), name='create'),
#   # url(r'^cart/(?P<slug>[-\d]+)/$', BuyItemLV.as_view(), name='detail'),

# )

urlpatterns = patterns('',
	url(r'^$', BuyLV.as_view(), name='buy_list'),
	url(r'^detail/(?P<slug>[-\w]+)/$', BuyDV.as_view(), name='buy_detail'),
	url(r'^detail/add$', create_buy, name='buy_add'),


	url(r'^cart/$', CartLV.as_view(), name='cart_list'),

	url(r'^item/add/(?P<slug>[-\w]+)/$', BuyItemCV.as_view(), name='buyitem_add'),
	url(r'^item/update/(?P<slug>[-\d]+)/(?P<pk>\d+)/$', BuyItemUV.as_view(), name='buyitem_update'),
	url(r'^item/delete/(?P<slug>[-\d]+)/(?P<pk>\d+)/$', BuyItemDelV.as_view(), name='buyitem_delete'),

	url(r'^cartitem/add/$', CartItemCV.as_view(), name='cartitem_add'),
	url(r'^cartitem/update/(?P<pk>\d+)/$', CartItemUV.as_view(), name='cartitem_update'),
	url(r'^cartitem/delete/(?P<pk>\d+)/$', CartItemDelV.as_view(), name='cartitem_delete'),

	url(r'^commit/(?P<slug>[-\w]+)/$', buy_commit, name='commit'),

	url(r'^narcotic/(?P<slug>[-\w]+)/$', NarcoticLV.as_view(), name='narcotic')
	

)


















