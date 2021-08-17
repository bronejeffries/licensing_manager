from rest_framework import viewsets
from rest_framework import permissions
from .serializers import LicenseSerializer, License
from rest_framework.generics import get_object_or_404, Http404
from rest_framework.response import Response
from rest_framework import mixins
from django.utils import timezone


class ActivationError(Exception):
    def __init__(self, *args):
        self.message = "Invalid License key.\nThis license is already activated.\nContact Software Vendor for support."
        super().__init__(self.message, *args)


class LicenseViewSet(viewsets.ReadOnlyModelViewSet, mixins.UpdateModelMixin):
    """
        API endpoint that allows licenses to be viewed or edited.
    """
    queryset = License.objects.all()
    serializer_class = LicenseSerializer
    # permission_classes = [permissions.IsAuthenticated]
    lookup_field = 'license_key'
    lookup_value_regex = '[-\w.]+'
    lookup_url_kwarg = lookup_field
    extra_get_look_up_field = 'license_secret_key'
    extra_get_url_look_up_kwargs = 's_key'

    """
    Retrieve a model instance.
    """

    def retrieve(self, request, *args, **url_kwargs):
        try:
            filter_kwargs = {self.lookup_field: url_kwargs[self.lookup_url_kwarg],
                             self.extra_get_look_up_field: request.GET[self.extra_get_url_look_up_kwargs]}
            instance = get_object_or_404(self.queryset, **filter_kwargs)
            serializer = self.get_serializer(instance)
            return Response(serializer.data)
        except KeyError:
            raise Http404

    """
    Update a model instance.
    """

    def update(self, request, *args, **url_kwargs):

        try:
            filter_kwargs = {self.lookup_field: url_kwargs[self.lookup_url_kwarg],
                             self.extra_get_look_up_field: request.GET[self.extra_get_url_look_up_kwargs]}
            instance = get_object_or_404(self.queryset, **filter_kwargs)
            if instance.activated:
                raise ActivationError
            serializer = self.get_serializer(instance, data={
                                             'activation_date': timezone.now(), 'activated': True}, partial=True)
            serializer.is_valid(raise_exception=True)
            self.perform_update(serializer)
            if getattr(instance, '_prefetched_objects_cache', None):
                # If 'prefetch_related' has been applied to a queryset, we need to
                # forcibly invalidate the prefetch cache on the instance.
                instance._prefetched_objects_cache = {}
            return Response({'code': 1, 'result': serializer.data, 'context': 'success', 'message': "Activated Sucessfully"})
        except KeyError:
            raise Http404
        except ActivationError as e:
            return Response({'message': str(e), 'code': 0, 'context': 'error'})
