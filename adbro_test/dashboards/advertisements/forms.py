from django import forms
from django.db import transaction

from adbro_test.apps.advertisements.model import (
    Advertiser, Campaign, AdvertisementGroup, AdvertisementGroupTargetingRule, Advertisement)
from adbro_test.apps.publishers.model import Publisher


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
            return advertisement
