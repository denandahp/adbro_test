from django import forms
from django.db import transaction

from adbro_test.apps.publishers.model import Publisher, Slot, Site


class CreateSlot(forms.ModelForm):
    class Meta:
        model = Slot
        fields = ['name']

    sites = forms.ModelMultipleChoiceField(
        label='Name Site',
        queryset=None,
        widget=forms.SelectMultiple,
        to_field_name='id')
    name = forms.CharField(label='Name Slot', max_length=255)

    def __init__(self, publisher: Publisher, *args, **kwargs):
        super().__init__(*args, **kwargs)
        self.is_update = self.instance.id
        self.fields['sites'].queryset = Site.objects.filter(publisher=publisher)
        if self.is_update:
            self.fields['sites'].initial = Site.objects.filter(guid=self.instance.site.guid)

    def save(self):
        if self.is_update:
            self.instance.name = self.cleaned_data.get('name')
            self.instance.save()
            return self.instance
        else:
            sites = self.cleaned_data['sites']
            name_slot  = self.cleaned_data['name']
            bulk_create_slots_list = []
            for site in sites:
                slot = Slot(site=site, name=name_slot)
                bulk_create_slots_list.append(slot)
            with transaction.atomic():
                if bulk_create_slots_list:
                    Slot.objects.bulk_create(bulk_create_slots_list)
                    return name_slot
                else:
                    return False


class CreateSite(forms.ModelForm):
    class Meta:
        model = Site
        fields = ['publisher', 'name']
        labels = {"publisher": "Name Publisher", 'name': 'Name Site'}

    def __init__(self, publisher: Publisher, *args, **kwargs):
        super().__init__(*args, **kwargs)
        self.is_update = self.instance.id
        self.fields['publisher'].initial = publisher
        if self.is_update:
            self.fields['publisher'].widget = forms.HiddenInput()


class CreatePublisher(forms.ModelForm):
    class Meta:
        model = Publisher
        fields = ['name']
        labels = {'name': 'Publisher Name'}

    site = forms.CharField(label='Site Name', max_length=255)
    slot = forms.CharField(label='Slot Name ', max_length=255)

    def __init__(self, *args, **kwargs):
        super().__init__(*args, **kwargs)
        self.is_update = self.instance.id
        if self.is_update:
            self.fields['name'].intial = self.instance.name
            self.fields['site'].widget = forms.HiddenInput()
            self.fields['slot'].widget = forms.HiddenInput()
            self.fields['site'].required = False
            self.fields['slot'].required = False

    def save(self, *args, **kwargs) -> Publisher:
        with transaction.atomic():
            if self.is_update:
                self.instance.name = self.cleaned_data.get('name')
                self.instance.save()
                return self.instance
            else:
                publisher = super().save(*args, **kwargs)
                site_name = self.cleaned_data.get('site')
                slot_name = self.cleaned_data.get('slot')
                site = Site.objects.create(publisher=publisher, name=site_name)
                Slot.objects.create(site=site, name=slot_name)
                return publisher