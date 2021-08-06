from .models import License
from rest_framework import serializers


class LicenseSerializer(serializers.ModelSerializer):
    client_name = serializers.CharField(source='client.name')

    class Meta:
        model = License
        fields = ("license_key", "license_secret_key", "client_name",
                  "license_type", "max_access_limit", 'created_on',
                  "activation_date", "life_span", "activated")
