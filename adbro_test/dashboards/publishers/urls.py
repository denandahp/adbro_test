from django.urls import path

from adbro_test.dashboards.publishers.views import (
    create_slot, create_site, index_publishers, create_publisher,
    index_sites, index_slots, update_publisher, update_site,
    update_slot
)

app_name = 'publishers'

urlpatterns = [
    path('index/publishers', index_publishers, name="index_publishers"),
    path('index/sites', index_sites, name="index_sites"),
    path('index/slots', index_slots, name="index_slots"),
    path('add/slot/<str:uuid_publisher>', create_slot, name="add_slot"),
    path('add/site/<str:uuid_publisher>', create_site, name="add_site"),
    path('add/publishers', create_publisher, name="add_publisher"),
    path('edit/slot/<str:uuid_slot>', update_slot, name="update_slot"),
    path('edit/site/<str:uuid_site>', update_site, name="update_site"),
    path('edit/publishers/<str:uuid_publisher>', update_publisher, name="update_publisher"),
]
