from django.contrib import messages
from django.shortcuts import render, redirect
from django.urls import reverse

from adbro_test.apps.publishers.model import Publisher, Site, Slot
from adbro_test.dashboards.publishers.forms import CreateSlot, CreateSite, CreatePublisher
from adbro_test.core.utils import PaginatorPage


def index_publishers(request):
    '''
    This function is to make index publisher with pagination
    '''
    page = request.GET.get('page', 1)
    limit = request.GET.get('limit', 10)
    publishers = Publisher.objects.all().order_by('name')
    paginator = PaginatorPage(publishers, page_number=page, step=limit, skip_step_calculation=True)
    context = {
        'title': 'Publishers',
        'objects': paginator.objects,
        'paginator': paginator,
        'active_tab': 'publisher',
        'active_sub_tab': 'publisher'
    }
    return render(request, 'dashboards/publishers/index_publisher.html', context)


def index_sites(request):
    '''
    This function is to make index publisher with pagination
    '''
    page = request.GET.get('page', 1)
    limit = request.GET.get('limit', 10)
    sites = Site.objects.all().order_by('name')
    paginator = PaginatorPage(sites, page_number=page, step=limit, skip_step_calculation=True)
    context = {
        'title': 'Sites',
        'objects': paginator.objects,
        'paginator': paginator,
        'active_tab': 'publisher',
        'active_sub_tab': 'site'
    }
    return render(request, 'dashboards/publishers/index_publisher.html', context)


def index_slots(request):
    '''
    This function is to make index publisher with pagination
    '''
    page = request.GET.get('page', 1)
    limit = request.GET.get('limit', 10)
    slots = Slot.objects.all().order_by('name')
    paginator = PaginatorPage(slots, page_number=page, step=limit, skip_step_calculation=True)
    context = {
        'title': 'Slots',
        'objects': paginator.objects,
        'paginator': paginator,
        'active_tab': 'publisher',
        'active_sub_tab': 'slot'
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
        'active_sub_tab': 'slot',
        'process': 'Create'
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
        'active_sub_tab': 'publisher',
        'process': 'Create'
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
        'active_sub_tab': 'publisher',
        'process': 'Create'

    }
    return render(request, 'dashboards/create.html', context)


def update_slot(request, uuid_slot: str):
    '''
    This function is to update slot
    '''
    slot = Slot.objects.select_related('site', 'site__publisher').filter(guid=uuid_slot).first()
    form = CreateSlot(data=request.POST or None,
                      instance=slot,
                      publisher=slot.site.publisher)
    if request.method == 'POST':
        if form.is_valid():
            site = form.save()
            messages.success(request, f'Update Site {site} success')
            return redirect(reverse('dashboards:publishers:index_slots'))

    context = {
        'form': form,
        'title': 'Update Slot',
        'active_tab': 'publisher',
        'active_sub_tab': 'slot',
        'process': 'Update'
    }
    return render(request, 'dashboards/create.html', context)


def update_site(request, uuid_site: str):
    '''
    This function is to update site
    '''
    site = Site.objects.get(guid=uuid_site)
    form = CreateSite(data=request.POST or None,
                      instance=site,
                      publisher=site.publisher)
    if request.method == 'POST':
        if form.is_valid():
            slot = form.save()
            messages.success(request, f'Update Slot {slot} success')
            return redirect(reverse('dashboards:publishers:index_sites'))

    context = {
        'form': form,
        'active_tab': 'publisher',
        'title': 'Update Site',
        'active_sub_tab': 'site',
        'process': 'Update'
    }
    return render(request, 'dashboards/create.html', context)


def update_publisher(request, uuid_publisher: str):
    '''
    This function is to update publisher
    '''
    publisher = Publisher.objects.get(guid=uuid_publisher)
    form = CreatePublisher(data=request.POST or None, instance=publisher)
    if request.method == 'POST':
        if form.is_valid():
            publisher = form.save()
            messages.success(request, f'Update Publisher {publisher} success')
            return redirect(reverse('dashboards:publishers:index_publishers'))

    context = {
        'form': form,
        'active_tab': 'publisher',
        'title': 'Update Publisher',
        'active_sub_tab': 'publisher',
        'process': 'Update'
    }
    return render(request, 'dashboards/create.html', context)
