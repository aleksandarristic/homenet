from django.db import models


class MenuURL(models.Model):
    objects = models.Manager()

    url = models.CharField(max_length=1024)
    text = models.CharField(max_length=100)

    created = models.DateTimeField('Created on', auto_now_add=True)
    updated = models.DateTimeField('Updated on', auto_now=True)
    active = models.BooleanField(default=True)
    order = models.PositiveSmallIntegerField(default=0)

    def __str__(self):
        return f'MenuURL(url="{self.url}", text="{self.text}")'

    class Meta:
        ordering = ['order']
