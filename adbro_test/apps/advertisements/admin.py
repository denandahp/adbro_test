from django.contrib import admin

from adbro_test.apps.advertisements.model import (
    Advertiser, Campaign, AdvertisementGroup, AdvertisementGroupTargetingRule, Advertisement)

admin.site.register(Advertiser)
admin.site.register(Campaign)
admin.site.register(AdvertisementGroup)
admin.site.register(AdvertisementGroupTargetingRule)
admin.site.register(Advertisement)
