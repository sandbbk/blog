from django.db import models
from django.utils import timezone
from mptt.models import MPTTModel, TreeForeignKey
from django.conf import settings


class Group(MPTTModel):
    parent = TreeForeignKey('self', null=True, max_length=64, verbose_name='Parent', blank=True, related_name='children', db_index=True)
    icon = models.ImageField(upload_to='', verbose_name=u'Photo', help_text='jpg/png - file')
    name = models.CharField(max_length=64)
    description = models.TextField(max_length=512, blank=True)

    def __str__(self):
        return self.name

    def icon_src(self):
         if self.icon:
             return r'<a href="{0}"><img src="{0}" width="30"/></a>'.format(self.icon.url)

    icon_src.allow_tags = True
    icon_src.short_description = 'Icon'

    class MPTTMeta:
        order_insertion_by = ['name']


class Element(models.Model):
    group = models.ForeignKey(Group, null=True, max_length=64, verbose_name='Group', db_index=True, related_name='relement')
    icon = models.ImageField(upload_to='', verbose_name=u'Photo', help_text='jpg/png - file')
    name = models.CharField(max_length=64)
    description = models.TextField(max_length=512)
    created_date = models.DateTimeField(default = timezone.now())
    is_modered = models.CharField(max_length=5,
                                  choices=(('null', 'null'), ('false', 'false'), ('true', 'true')), default='null')

    def __str__(self):
        return self.name

    def icon_src(self):
        if self.icon:
            return r'<img src="%s" height ="30">' % self.icon.url

    icon_src.allow_tags = True
    icon_src.short_description = 'Icon'
