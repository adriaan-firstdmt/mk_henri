from rest_framework import viewsets
from rest_framework import permissions
from rest_framework import status as responseStatus
from rest_framework.decorators import action
from rest_framework.response import Response
from rest_framework import filters
from django.http import HttpResponseRedirect
from tr069server.models import Device
from tr069server.serializers import DeviceSerializer


# Create your views here.
def home_redirect_view(request):
    return HttpResponseRedirect('/admin/')


class DeviceViewSet(viewsets.ModelViewSet):
    queryset = Device.objects.all()
    serializer_class= DeviceSerializer
    permission_classes = [permissions.IsAuthenticated]

    search_fields = ['ip']
    filter_backends = (filters.SearchFilter,)

    @action(detail=False, methods=["POST"])
    def set_status(self,request) -> Response:
        """ Custom api action that sets the status of a device found by IP address if IP"""
        ip = request.data['ip']
        status = request.data['status']
        device_query = Device.objects.filter(ip=ip)

        if device_query.count() != 1:
            return Response({'success':False, "status_changed":False },status=responseStatus.HTTP_404_NOT_FOUND)

        device = device_query.get()
        device.provisioningstatus.status = status
        device.provisioningstatus.save()

        return Response({'success':True, "status_changed":device.provisioningstatus.status },status=responseStatus.HTTP_200_OK)
    


    # # TODO Add api to provision device
    # @action(detail=False, methods=["get","post"])
    # def provision_device(self,request) -> Response:
    #     ip = request.data['ip']
    #     device_query = Device.objects.filter(ip=ip)

    #     if device_query.count() != 1:
    #         return Response({'success':True, "status_changed":False },status=status.HTTP_404_NOT_FOUND)
        
    #     return Response({'success':True, "status_changed":True },status=status.HTTP_200_OK)