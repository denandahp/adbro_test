from django import forms

from adbro_test.apps.publishers.model import Publisher, Slot, Site


class CreateSlot(forms.Form):
    sites = forms.ModelMultipleChoiceField(
        label='Name Site',
        queryset=None,
        widget=forms.SelectMultiple,
        to_field_name='id')
    slot = forms.CharField(label='Name Slot', max_length=255)

    def __init__(self, publisher: Publisher, *args, **kwargs):
        super().__init__(*args, **kwargs)
        self.fields['sites'].queryset = Site.objects.filter(publisher=publisher)

    def save(self):
        sites = self.cleaned_data['sites']
        name_slot  = self.cleaned_data['slot']
        bulk_create_slots_list = []
        for site in sites:
            slot = Slot(site=site, name=name_slot)
            bulk_create_slots_list.append(slot)
        
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
        self.fields['publisher'].initial = publisher
