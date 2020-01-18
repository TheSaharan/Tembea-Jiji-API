from django.db import models

from django.utils.translation import ugettext as _


class BusStop(models.Model):
    stop_name = models.CharField(max_length=200, blank=False, null=False)
    lat = models.FloatField(_('Latitude'), blank=False, null=False)
    lon = models.FloatField(_('Longitude'), blank=False, null=False)

    def __str__(self):
        return "Bus stop at: {}".format(self.stop_name)

    class Meta:
        ordering = ('stop_name'),


class Stage(models.Model):
    stage_name = models.CharField(max_length=200, blank=False, null=False)
    lat = models.FloatField(_('Latitude'), blank=False, null=False)
    lon = models.FloatField(_('Longitude'), blank=False, null=False)

    def __str__(self):
        return "Stage: {} ".format(self.stage_name)

    class Meta:
        ordering = ('stage_name'),


class Route(models.Model):
    name = models.CharField(max_length=5, blank=False, null=False)
    stops = models.ManyToManyField(BusStop)
    stages = models.ManyToManyField(Stage)

    def __str__(self):
        return self.name

    class Meta:
        ordering = ('name'),
