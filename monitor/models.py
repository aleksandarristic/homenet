from django.db import models
from django.utils import timezone as tz


class Device(models.Model):
    objects = models.Manager()

    name = models.CharField(max_length=30, blank=True)
    description = models.TextField(blank=True)
    type = models.CharField(max_length=20, default="DEVICE")

    first_seen = models.DateTimeField("First seen", default=tz.now)
    last_seen = models.DateTimeField("Last seen", default=tz.now)

    mac_address = models.CharField(max_length=17)
    manufacturer = models.TextField(blank=True)
    last_ip = models.GenericIPAddressField("Last known IP")

    def __str__(self):
        return f'Device("{self.name}", "{self.mac_address}", "{self.last_ip}", {self.last_seen})'

    class Meta:
        ordering = ['-last_seen']


class Scan(models.Model):
    objects = models.Manager()

    devices = models.ManyToManyField(Device)

    time = models.DateTimeField(auto_now_add=True)
    type = models.CharField(max_length=20)
    output = models.TextField(blank=True, null=True, default=None)
    command = models.CharField(max_length=255)
    running = models.BooleanField(default=False)

    def __str__(self):
        return f'Scan("{self.type}", "{self.time}")'

    class Meta:
        ordering = ['-time']
