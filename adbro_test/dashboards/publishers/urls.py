from django.urls import path

from adbro_test.dashboards.publishers.views import (
    create_slot, create_site, index_publisher, create_publisher
)

app_name = 'publishers'

urlpatterns = [
    # path('', index, name='index'),
    path('', index_publisher, name="index_publishers"),
    path('add/slot/<str:uuid_publisher>', create_slot, name="add_slot"),
    path('add/site/<str:uuid_publisher>', create_site, name="add_site"),
    path('add/publisher', create_publisher, name="add_publisher"),
]
