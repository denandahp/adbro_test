import uuid

from django.db import models


class Publisher(models.Model):
    guid = models.UUIDField(unique=True, default=uuid.uuid4, editable=False)
    name = models.CharField(max_length=255)
    created = models.DateTimeField(auto_now_add=True)
    updated = models.DateTimeField(auto_now=True)

    def __str__(self) -> str:
        return self.name

class Site(models.Model):
    guid = models.UUIDField(unique=True, default=uuid.uuid4, editable=False)
    publisher = models.ForeignKey(Publisher, related_name='sites', on_delete=models.CASCADE)
    name = models.CharField(max_length=255)
    created = models.DateTimeField(auto_now_add=True)
    updated = models.DateTimeField(auto_now=True)

    def __str__(self) -> str:
        return self.name

class Slot(models.Model):
    guid = models.UUIDField(unique=True, default=uuid.uuid4, editable=False)
    site = models.ForeignKey(Site, related_name='slots', on_delete=models.CASCADE)
    name = models.CharField(max_length=255)
    created = models.DateTimeField(auto_now_add=True)
    updated = models.DateTimeField(auto_now=True)

    def __str__(self) -> str:
        return self.name