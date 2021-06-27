from django.db import models
from django.utils import timezone


class LoanApplication(models.Model):

    NEW_STATUS = 1
    REJECTED_STATUS = 2
    APPROVED_STATUS = 3
    STATUS_CHOICES = (
        (NEW_STATUS, 'New'),
        (REJECTED_STATUS, 'Rejected'),
        (APPROVED_STATUS, 'Approved'),
    )
    id = models.AutoField(primary_key=True)
    name = models.CharField(max_length=200, null=True)
    surname = models.CharField(max_length=255, null=True)
    phone = models.CharField(max_length=200, null=True)
    email = models.CharField(max_length=200, null=True)
    date_created = models.DateTimeField(auto_now_add=True, null=True)

    amount = models.DecimalField(max_digits=20, decimal_places=2)
    term = models.IntegerField(null=True)
    rate = models.DecimalField(max_digits=20, decimal_places=2)
    description = models.CharField(max_length=200, null=True, blank=True)

    status = models.IntegerField(choices=STATUS_CHOICES, default=NEW_STATUS)

    class Meta:
        verbose_name = "Client"
        verbose_name_plural = "Clients"

    def __init__(self, *args, **kwargs):
        super().__init__(*args, **kwargs)
        self.id = None

    def __str__(self):
        return self.name
