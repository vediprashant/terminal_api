from rest_framework import generics

from apps.endpoints import (
    models as endpoint_models,
    serializers as endpoints_serializers,
    utils as endpoint_utils
)


class EndpointView(generics.ListCreateAPIView):
    """
    View to Create and List URL's
    """
    queryset = endpoint_models.Endpoint.objects.all().order_by('-created_at')
    serializer_class = endpoints_serializers.EndpointSerializer

    def get_queryset(self):
        endpoint_utils.update_expiration_field()
        url_qs = super().get_queryset()
        return url_qs.filter(is_expired=False)


class EndPointDetailView(generics.ListCreateAPIView):
    """
    View to handle Request to a Specific Url
    """
    queryset = endpoint_models.EndpointDetail.objects.all()
    serializer_class = endpoints_serializers.EndpointDetailSerializer

    def get_serializer_context(self):
        context = super().get_serializer_context()
        context['headers'] = self.request.headers
        context['query_params'] = self.request.GET
        context['kwargs'] = self.kwargs.get('url')
        return context
    
    def get_queryset(self):
        endpoint_utils.update_expiration_field()
        url_detail_qs = super().get_queryset()
        url_detail_qs = url_detail_qs.filter(endpoint__url=self.kwargs.get('url'), endpoint__is_expired=False)
        return url_detail_qs.order_by('-created_at')[:5]
