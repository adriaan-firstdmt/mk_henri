from django.shortcuts import render
from django.contrib.auth.models import User, Group

from rest_framework import viewsets
from rest_framework import permissions
from rest_framework import status
from rest_framework.decorators import action
from rest_framework.response import Response
from tr069server.models import Device

from tr069server.serializers import UserSerializer, DeviceSerializer

# Create your views here.
class UserViewSet(viewsets.ModelViewSet):
    """
    API endpoint that allows users to be viewed or edited.
    """
    queryset = User.objects.all().order_by('-date_joined')
    serializer_class = UserSerializer
    permission_classes = [permissions.IsAuthenticated]


class DeviceViewSet(viewsets.ModelViewSet):
    queryset = Device.objects.all()
    serializer_class= DeviceSerializer
    permission_classes = [permissions.IsAuthenticated]
    lookup_field = 'customer_code'

    @action(detail=True, methods=["get"])
    def set_status_true(self,request,customer_code):
        device = Device.objects.filter(customer_code=customer_code).get()
        device.provisioningstatus.status = True
        device.provisioningstatus.save()
        changed_status = device.ip
        return Response({'success':True, "status_changed":device.provisioningstatus.status },status=status.HTTP_200_OK)
        