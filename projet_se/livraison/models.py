from django.db import models
from django.utils.translation import gettext_lazy as _
from commande.models import Commande
from random import randint
import qrcode
import os
from django.db import models
from django.db.models import Max
from django.utils.translation import gettext_lazy as _
from commande.models import Commande
from random import randint
import qrcode
import os


def generate_tracking_number():
    return f"TRK{randint(1000, 9999)}"


def generate_qr_code_path(instance, filename):
    return os.path.join('qr_codes', f"{instance.tracking_number}.png")



class Livraison(models.Model):
    class DeliveryState(models.TextChoices):
        PENDING = 'Pending', _('Pending')
        IN_TRANSIT = 'In Transit', _('In Transit')
        DELIVERED = 'Delivered', _('Delivered')
        FAILED = 'Failed', _('Failed')

    id = models.AutoField(primary_key=True)
    incremental_id = models.IntegerField(editable=False, null=True, unique=True)
    commande = models.ForeignKey(
        Commande,
        on_delete=models.CASCADE,
        related_name='livraisons',
        verbose_name=_('Commande')
    )
    state = models.CharField(
        max_length=20,
        choices=DeliveryState.choices,
        default=DeliveryState.PENDING,
        verbose_name=_('State')
    )
    delivery_date = models.DateTimeField(
        null=True,
        blank=True,
        verbose_name=_('Delivery Date')
    )
    tracking_number = models.CharField(
        max_length=10,
        unique=True,
        default="",
        verbose_name=_('Tracking Number')
    )
    created_at = models.DateTimeField(auto_now_add=True, verbose_name=_('Created At'))
    updated_at = models.DateTimeField(auto_now=True, verbose_name=_('Updated At'))
    qr_path = models.ImageField(
        upload_to='qr_codes/',
        null=True,
        blank=True,
        verbose_name=_('QR Code Path')
    )

    def save(self, *args, **kwargs):
        # Set the incremental ID
        if self.incremental_id is None:
            max_id = Livraison.objects.aggregate(Max('incremental_id'))['incremental_id__max'] or 0
            self.incremental_id = max_id + 1

        # Set the tracking number if not provided
        if not self.tracking_number:
            self.tracking_number = f"TRK{randint(1000, 9999)}"

        super().save(*args, **kwargs)

    class Meta:
        verbose_name = _('Livraison')
        verbose_name_plural = _('Livraisons')
        ordering = ['-created_at']

    def __str__(self):
        return f"Livraison {self.incremental_id} - Commande {self.commande.id}"