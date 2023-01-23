from django.db import models


class DenormalizedAdvertisement(models.Model):
    advertisement = models.UUIDField(blank=False, null=False, editable=False)
    group = models.UUIDField(blank=False, null=False, editable=False)
    campaign = models.UUIDField(blank=False, null=False, editable=False)
    site = models.UUIDField(blank=False, null=False, editable=False)
    slot = models.UUIDField(blank=False, null=False, editable=False)
    tags = models.CharField(max_length=255, blank=True, null=True)
    data = models.TextField(blank=True, null=True)
    created = models.DateTimeField(auto_now_add=True)
    updated = models.DateTimeField(auto_now=True)

    class Meta:
        managed = False
        db_table='denormalized_advertisement'