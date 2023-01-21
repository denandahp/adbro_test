from django.contrib import messages
from django.shortcuts import render, redirect
from django.urls import reverse

from adbro_test.apps.publishers.model import Publisher
from adbro_test.apps.advertisement_views.model import DenormalizedAdvertisement
from adbro_test.dashboards.advertisements.forms import CreateAdvertisement
from adbro_test.core.utils import PaginatorPage


def index_advertisement(request):
    page = request.GET.get('page', 1)
    limit = request.GET.get('limit', 10)
    advertisements = DenormalizedAdvertisement.objects.all().order_by('-created')
    paginator = PaginatorPage(advertisements, page_number=page, step=limit, skip_step_calculation=True)
    context = {
        'title': 'Advertisement',
        'advertisements': paginator.objects,
        'paginator': paginator,
        'active_tab': 'advertisement',
    }
    return render(request, 'dashboards/advertisements/index.html', context)


def create_advertisement(request):
    form = CreateAdvertisement(data=request.POST or None)

    if request.method == 'POST':
        if form.is_valid():
            advertisement = form.save()
            messages.success(request, f'Create Site {advertisement} success')
            return redirect(reverse('dashboards:advertisements:index_advertisement'))

    context = {
        'form': form,
        'active_tab': 'advertisement',
        'title': 'Add Advertisement',
    }
    return render(request, 'dashboards/create.html', context)
