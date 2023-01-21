from django.urls import path, include

app_name = 'dashboards'

urlpatterns = [
    path('publishers/', include(
        'adbro_test.dashboards.publishers.urls', namespace='publishers')),
    path('advertisements/', include(
        'adbro_test.dashboards.advertisements.urls', namespace='advertisements')),
]