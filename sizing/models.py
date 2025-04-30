from django.db import models
from django.conf import settings

class Appliance(models.Model):
    name = models.CharField(max_length=100)
    watts = models.FloatField(help_text="Power consumption in watts")
    default_hours_per_day = models.FloatField(
        help_text="Typical usage time per day in hours"
    )

    def __str__(self):
        return self.name


class SystemDesign(models.Model):
    user = models.ForeignKey(
        settings.AUTH_USER_MODEL,
        null=True,
        blank=True,
        on_delete=models.SET_NULL,
        help_text="Optional—link to Django user if you implement authentication"
    )
    latitude = models.DecimalField(
        max_digits=8,
        decimal_places=5,
        help_text="Site latitude"
    )
    longitude = models.DecimalField(
        max_digits=8,
        decimal_places=5,
        help_text="Site longitude"
    )
    panel_watts = models.IntegerField(
        help_text="Recommended PV array wattage"
    )
    battery_ah = models.IntegerField(
        help_text="Recommended battery capacity (Ah)"
    )
    created_at = models.DateTimeField(auto_now_add=True)

    def __str__(self):
        user = self.user.username if self.user else "Anonymous"
        return f"Design #{self.id} by {user}"


class Calculation(models.Model):
    system_design = models.ForeignKey(
        SystemDesign,
        related_name='calculations',
        on_delete=models.CASCADE
    )
    daily_load_wh = models.FloatField(help_text="Total daily load in Wh")
    sun_hours = models.FloatField(help_text="Average sun-hours/day")
    panel_w = models.IntegerField(help_text="Calculated PV array wattage")
    battery_ah = models.IntegerField(help_text="Calculated battery capacity (Ah)")
    calculated_at = models.DateTimeField(auto_now_add=True)

    def __str__(self):
        return f"Calc #{self.id} for Design #{self.system_design.id}"
