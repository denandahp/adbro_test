from django.contrib import messages
from django.shortcuts import render, redirect
from django.urls import reverse

from adbro_test.apps.publishers.model import Publisher
from adbro_test.dashboards.publishers.forms import CreateSlot, CreateSite, CreatePublisher
from adbro_test.core.utils import PaginatorPage


def index_publisher(request):
    '''
    This function is to make index publisher with pagination
    '''
    page = request.GET.get('page', 1)
    limit = request.GET.get('limit', 10)
    publishers = Publisher.objects.all().order_by('name')
    paginator = PaginatorPage(publishers, page_number=page, step=limit, skip_step_calculation=True)
    context = {
        'title': 'Publishers',
        'publishers': paginator.objects,
        'paginator': paginator,
        'active_tab': 'publisher',
    }
    return render(request, 'dashboards/publishers/index_publisher.html', context)


def create_slot(request, uuid_publisher: str):
    '''
    This function is to create new slot with existing publisher and site
    '''
    publisher = Publisher.objects.get(guid=uuid_publisher)
    form = CreateSlot(data=request.POST or None, publisher=publisher)
    if request.method == 'POST':
        if form.is_valid():
            site = form.save()
            messages.success(request, f'Create Site {site} success')
            return redirect(reverse('dashboards:publishers:index_publishers'))

    context = {
        'form': form,
        'title': 'Add Slot',
        'active_tab': 'publisher',
    }
    return render(request, 'dashboards/create.html', context)


def create_site(request, uuid_publisher: str):
    '''
    This function is to create new site with existing publisher
    '''
    publisher = Publisher.objects.get(guid=uuid_publisher)
    form = CreateSite(data=request.POST or None, publisher=publisher)
    if request.method == 'POST':
        if form.is_valid():
            slot = form.save()
            messages.success(request, f'Create Slot {slot} success')
            return redirect(reverse('dashboards:publishers:index_publishers'))

    context = {
        'form': form,
        'active_tab': 'publisher',
        'title': 'Add Site',
    }
    return render(request, 'dashboards/create.html', context)


def create_publisher(request):
    '''
    This function is to create new publisher
    '''
    form = CreatePublisher(data=request.POST or None)
    if request.method == 'POST':
        if form.is_valid():
            publisher = form.save()
            messages.success(request, f'Create Publisher {publisher} success')
            return redirect(reverse('dashboards:publishers:index_publishers'))

    context = {
        'form': form,
        'active_tab': 'publisher',
        'title': 'Add Publisher',
    }
    return render(request, 'dashboards/create.html', context)
