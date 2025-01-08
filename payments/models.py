from django.db import models
from django.utils.translation import gettext_lazy as _

class Plan(models.Model):
    class DuratuonType(models.TextChoices):
        Month = 'Month', _('Month')
        Day = 'Day', _('Day')
        Year = 'Year', _('Year')
        
    class Storage(models.TextChoices):
        GB = 'GB', _('GB')
        MB = 'MB', _('MB')
    name = models.CharField(max_length=100)  # e.g., "Free", "Pro"
    price = models.DecimalField(max_digits=10, decimal_places=2)  # e.g., $10.00
    data_limit = models.DecimalField(max_digits=20, decimal_places=10)  # e.g., 1.123456789 GB
    data_type = models.CharField(max_length=50, choices=Storage.choices,default='MB')
    duration = models.PositiveIntegerField()  # Duration in days or months
    duration_type = models.CharField(max_length=50, choices=DuratuonType.choices,default='Day')

    def __str__(self):
        return self.name
        
        


class UserSubscription(models.Model):
    user = models.OneToOneField('accounts.Patient', on_delete=models.CASCADE)
    plan = models.ForeignKey(Plan, on_delete=models.SET_NULL, null=True)
    data_used = models.DecimalField(max_digits=20, decimal_places=10)  # e.g., 1.123456789 GB
    plan_start_date = models.DateField()
    plan_end_date = models.DateField()
    active = models.BooleanField(default=True)

    def is_within_limit(self):
        return self.data_used <= self.plan.data_limit