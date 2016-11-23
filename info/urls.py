from django.conf.urls import url,patterns, include
from .views import *


urlpatterns = patterns(
    # Examples:
    # url(r'^$', 'StockAdmin.views.home', name='home'),
    # url(r'^blog/', include('blog.urls')),

   url(r'^$', IndexTV.as_view(), name='index'),
	url(r'^updateForm/$', DrugInfoFromXlFile.as_view(), name='updatexl')
)
