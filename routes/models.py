from django.db import models

from django.utils.translation import ugettext as _

class Route(models.Model):
    route_number = models.CharField(max_length=5, blank=False, null=False)

    def __str__(self):
        return self.route_number

    class Meta:
        ordering = ('route_number'),


class BusStop(models.Model):
    route = models.ForeignKey('Route', on_delete=models.CASCADE)
    stop_name = models.CharField(max_length=200, blank=False, null=False)
    lat = models.FloatField(_('Latitude'), blank=False, null=False)
    lon = models.FloatField(_('Longitude'), blank=False, null=False)

    def __str__(self):
        return "stop: {} for Matatu route number: {}".format(self.stop_name, self.route.route_number)


class Stage(models.Model):
    route = models.ForeignKey('Route', on_delete=models.CASCADE)
    stage_name = models.CharField(max_length=200, blank=False, null=False)
    lat = models.FloatField(_('Latitude'), blank=False, null=False)
    lon = models.FloatField(_('Longitude'), blank=False, null=False)

    def __str__(self):
        return "Stage: {} for Matatu route number: {}".format(self.stage_name, self.route.route_number)
