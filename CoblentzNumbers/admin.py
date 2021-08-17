from django.contrib import admin
from .models import CoblentzNumbers

class CoblentzNumbersAdmin(admin.ModelAdmin):
    pass
   # readonly_fields = ('created',)

admin.site.register(CoblentzNumbers, CoblentzNumbersAdmin)