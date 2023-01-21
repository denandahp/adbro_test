from django import forms
from django.db import transaction

from adbro_test.apps.advertisement_views.model import DenormalizedAdvertisement
from adbro_test.apps.advertisements.model import (
    Advertiser, Campaign, AdvertisementGroup, AdvertisementGroupTargetingRule, Advertisement)
from adbro_test.apps.publishers.model import Slot, Publisher


class CreateAdvertisement(forms.Form):
    advertiser = forms.CharField(label='Name Advertiser', max_length=255)
    campaign = forms.CharField(label='Name Campaign', max_length=255)
    advertisement = forms.CharField(label='Advertisement', widget=forms.Textarea())
    advertisement_group = forms.CharField(label='Advertisement Group', max_length=255)
    tags = forms.CharField(label='Tags', max_length=255)
    description = forms.CharField(label='Description', required=False)
    Publisher = forms.ModelMultipleChoiceField(
        label='Name Publisher',
        queryset=None,
        widget=forms.SelectMultiple,
        to_field_name='id')

    def __init__(self, *args, **kwargs):
        super().__init__(*args, **kwargs)
        self.fields['Publisher'].queryset = Publisher.objects.all()
    
    def clean(self):
        data = super().clean()
        if self.errors:
            return data
        publishers = data.get('Publisher')
        self.slots = Slot.objects.select_related('site').filter(site__publisher__in=publishers)
        if not self.slots:
            error = forms.ValidationError('Slots is empty', code="invalid_Publisher")
            self.add_error('Publisher', error)
        return data

    def save(self):
        with transaction.atomic():
            advertiser = Advertiser.objects.create(name=self.cleaned_data.get('advertiser'))
            campaign = Campaign.objects.create(advertiser=advertiser, name=self.cleaned_data.get('advertiser'))
            advertisement_group = AdvertisementGroup.objects.create(campaign=campaign, 
                                                                    name=self.cleaned_data.get('advertisement_group'))
            AdvertisementGroupTargetingRule.objects.create(advertisement_group=advertisement_group,
                                                        tags=self.cleaned_data.get('tags'),
                                                        description=self.cleaned_data.get('description'))
            advertisement = Advertisement.objects.create(advertisement_group=advertisement_group,
                                                        data=self.cleaned_data.get('advertisement'))
            bulk_create_denormalized_advertisements = []
            for slot in self.slots:
                denormalized_advertisement = DenormalizedAdvertisement(
                    advertisement=advertisement.guid,
                    group=advertisement_group.guid,
                    campaign=campaign.guid,
                    site=slot.site.guid,
                    slot=slot.guid,
                    tags=self.cleaned_data.get('tags'),
                    data=self.cleaned_data.get('advertisement')
                )
                bulk_create_denormalized_advertisements.append(denormalized_advertisement)
            if bulk_create_denormalized_advertisements:
                    DenormalizedAdvertisement.objects.bulk_create(bulk_create_denormalized_advertisements)
            
            return advertisement



