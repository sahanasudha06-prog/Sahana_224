
from django.db import models
from datetime import date
from dateutil.relativedelta import relativedelta


class Member(models.Model):
    MEMBERSHIP_CHOICES = [
        ('Monthly', 'Monthly'),
        ('Quarterly', 'Quarterly'),
        ('Yearly', 'Yearly'),
    ]

    name = models.CharField(max_length=100)
    email = models.EmailField(unique=True)
    phone = models.CharField(max_length=15)

    membership_type = models.CharField(
        max_length=20,
        choices=MEMBERSHIP_CHOICES
    )

    joining_date = models.DateField()
    expiry_date = models.DateField(null=True, blank=True)
    is_active = models.BooleanField(default=True)

    def save(self, *args, **kwargs):
        if self.joining_date:
            if self.membership_type == 'Monthly':
                duration = relativedelta(months=1)
            elif self.membership_type == 'Quarterly':
                duration = relativedelta(months=3)
            else:
                duration = relativedelta(years=1)

            self.expiry_date = self.joining_date + duration

        super().save(*args, **kwargs)

    def __str__(self):
        return self.name
