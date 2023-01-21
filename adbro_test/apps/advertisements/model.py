import uuid

from django.db import models

from adbro_test.apps.publishers.model import Slot

class Advertiser(models.Model):
    guid = models.UUIDField(unique=True, default=uuid.uuid4, editable=False)
    name = models.CharField(max_length=255)
    created = models.DateTimeField(auto_now_add=True)
    updated = models.DateTimeField(auto_now=True)

    def __str__(self) -> str:
        return self.name

class Campaign(models.Model):
    guid = models.UUIDField(unique=True, default=uuid.uuid4, editable=False)
    advertiser = models.ForeignKey(Advertiser, on_delete=models.CASCADE, related_name='campaigns')
    name = models.CharField(max_length=255)
    created = models.DateTimeField(auto_now_add=True)
    updated = models.DateTimeField(auto_now=True)

    def __str__(self) -> str:
        return self.name

class AdvertisementGroup(models.Model):
    guid = models.UUIDField(unique=True, default=uuid.uuid4, editable=False)
    campaign = models.ForeignKey(Campaign, on_delete=models.CASCADE, related_name='advertisement_groups')
    name = models.CharField(max_length=255)
    created = models.DateTimeField(auto_now_add=True)
    updated = models.DateTimeField(auto_now=True)

    def __str__(self) -> str:
        return self.name

class AdvertisementGroupTargetingRule(models.Model):
    advertisement_group = models.ForeignKey(AdvertisementGroup, on_delete=models.CASCADE, related_name='targeting_rules')
    slot = models.ManyToManyField(Slot, related_name='targeting_rules', blank=True)
    tags = models.CharField(max_length=255)
    description = models.CharField(max_length=255, blank=True, null=True)
    created = models.DateTimeField(auto_now_add=True)
    updated = models.DateTimeField(auto_now=True)

    def __str__(self) -> str:
        return self.tags

class Advertisement(models.Model):
    guid = models.UUIDField(unique=True, default=uuid.uuid4, editable=False)
    advertisement_group = models.ForeignKey(AdvertisementGroup, related_name='advertisements', on_delete=models.CASCADE)
    data = models.TextField()
    created = models.DateTimeField(auto_now_add=True)
    updated = models.DateTimeField(auto_now=True)
