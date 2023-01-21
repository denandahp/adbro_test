from django.contrib import admin

from adbro_test.apps.publishers.model import Publisher, Site, Slot

admin.site.register(Publisher)
admin.site.register(Site)
admin.site.register(Slot)
