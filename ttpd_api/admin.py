from django.contrib import admin

from ttpd_admin.models import Commodities, Industries, Sectors


admin.site.register(Commodities)
admin.site.register(Industries)
admin.site.register(Sectors)
