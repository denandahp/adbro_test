from django.urls import path

from adbro_test.dashboards.advertisements.views import (
    index_advertisement, create_advertisement
)

app_name = 'advertisements'

urlpatterns = [
    path('', index_advertisement, name="index_advertisement"),
    path('add', create_advertisement, name="create_advertisement"),
]
