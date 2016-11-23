from django.contrib import admin
from .models import Info, Account

# Register your models here.


class AcountAdmin(admin.ModelAdmin):
    '''
        Admin View for Acount
    '''
    list_display = ('name','tel','email','address',)
admin.site.register(Account, AcountAdmin)

class InfoAdmin(admin.ModelAdmin):
    '''
        Admin View for Info
    '''
    list_display = ('firm','edi','name','total_stockin_amount','base_amount','current_stock','standard_unit','narcotic_class',)
    list_filter = ('narcotic_class',)
    search_fields = ('name',)
admin.site.register(Info, InfoAdmin)

