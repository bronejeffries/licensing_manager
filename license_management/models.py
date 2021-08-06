from django.db import models
from django.core.exceptions import ValidationError
import uuid
from django.utils.translation import gettext_lazy as _
import secrets
from django.conf import settings
# Create your models here.


def generate_key():
    return f"{uuid.uuid4()}-{secrets.token_urlsafe(160)}"


class Client(models.Model):
    """
        client data representation
    """
    name = models.CharField(max_length=150, null=False, blank=False)
    address = models.CharField(max_length=150, null=False, blank=False)
    contact = models.CharField(max_length=150, null=False, blank=False)
    public_key = models.TextField()
    created_by = models.ForeignKey(
        settings.AUTH_USER_MODEL, on_delete=models.CASCADE)
    created_at = models.DateField(auto_now_add=True)

    class Meta:
        constraints = [models.UniqueConstraint(
            fields=['public_key', 'name'], name="Client and public key constraint")]

    def __repr__(self):
        return f"{self.name}"

    def __str__(self):
        return f"{self.name}"


class License(models.Model):
    """
        license data table representation
    """

    License_type_choices = models.TextChoices("LicenseType",
                                              ("Concurrent", "Named"))

    license_key = models.TextField(
        editable=False, default=generate_key, unique=True)
    license_secret_key = models.UUIDField(
        editable=False, default=uuid.uuid4, unique=True)
    client = models.ForeignKey(
        Client, on_delete=models.CASCADE, help_text="License owner", null=True)

    license_type = models.CharField(
        max_length=25, choices=License_type_choices.choices)

    max_access_limit = models.IntegerField(
        null=False, default=1, help_text="max no. of users allowed")

    created_on = models.DateTimeField(auto_now_add=True)

    activation_date = models.DateTimeField(
        null=True, help_text="optional, activation date", blank=True)

    activated = models.BooleanField(null=False, default=False)

    life_span = models.IntegerField(
        default=1, null=False, help_text="period in days that the license is valid")  # in days

    def __repr__(self):
        return f" client: {self.client.name}, key_created_on: {self.created_on}"

    def __str__(self):
        return f" client: {self.client.name}, key_created_on: {self.created_on}"

    def clean(self):
        # validate mac addresses against limit
        # if len(self.allowed_mac_addresses.split(",")) != self.max_access_limit:
        #     raise ValidationError({
        #         'allowed_mac_addresses': _('Mac addresses should be the exact suggested limit.')
        #     })
        if self.license_type == "Named" and self.max_access_limit != 1:
            raise ValidationError({
                'max_access_limit': _('Maximum number of users is one (1) for this license type.')
            })

        if self.license_type == "Concurrent" and self.max_access_limit <= 1:
            raise ValidationError({
                'max_access_limit': _('Maximum number of users must be more than one (1) for this license type.')
            })

    def save(self, *args, **kwargs):

        # clean mac addresses
        # self.allowed_mac_addresses = ",".join(
        #     [mac.strip() for mac in self.allowed_mac_addresses.split(",")]
        # )
        # end clean

        if self.license_type == "Named":
            self.max_access_limit = 1

        super().save(*args, **kwargs)
