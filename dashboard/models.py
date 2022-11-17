from django.db import models


class BaseModel(models.Model):
    objects = models.Manager()

    text = models.CharField(max_length=100)
    order = models.PositiveSmallIntegerField(default=0)
    active = models.BooleanField(default=True)

    created = models.DateTimeField('Created on', auto_now_add=True)
    updated = models.DateTimeField('Updated on', auto_now=True)

    class Meta:
        abstract = True


class UrlGroup(BaseModel):
    name = models.CharField(max_length=64)

    def __str__(self):
        return f'URLGroup(name="{self.name}", text="{self.text}")'

    def active_menu_items(self):
        return self.menuurl_set.filter(active=True)

    class Meta:
        ordering = ['order']


class MenuURL(BaseModel):
    url = models.CharField(max_length=1024)
    new_window = models.BooleanField('Open in new window', default=False, null=True)
    url_group = models.ForeignKey(UrlGroup, on_delete=models.SET_NULL, blank=True, null=True)
    post_request = models.BooleanField('Make this link a post request', default=False, null=True)
    post_warning = models.CharField(max_length=1024, default='', null=True, blank=True)

    def __str__(self):
        return f'MenuURL(url="{self.url}", text="{self.text}")'

    class Meta:
        ordering = ['order']

