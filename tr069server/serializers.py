from django.contrib.auth.models import User, Group
from tr069server.models import Device,ProvisioningStatus
from rest_framework import serializers


class UserSerializer(serializers.HyperlinkedModelSerializer):
    class Meta:
        model = User
        fields = ['url', 'username', 'email', 'groups']


class DeviceSerializer(serializers.HyperlinkedModelSerializer):
    class Meta:
        model = Device
        fields = ['ip', 'customer_code']
