from django.utils import timezone
from rest_framework import serializers

from apps.endpoints import (
     constants as endpoint_constants,
     models as endpoint_models
)


class EndpointSerializer(serializers.ModelSerializer):
    """
    Serializer to Create and List Url's
    """
    expiration_time_left = serializers.SerializerMethodField()

    class Meta:
        model = endpoint_models.Endpoint
        fields = ['url', 'is_expired', 'expiration_time_left']
        read_only_fields = ['url', 'is_expired']

    def get_expiration_time_left(self, instance):
        time_left = (
            endpoint_constants.EXPIRATION_TIME_IN_SECONDS - (
                timezone.now() - instance.created_at
            ).total_seconds()
        )
        return time_left


class EndpointDetailSerializer(serializers.ModelSerializer):
    """
    Serializer to handle data posted to the url
    """
    expiration_time_left = serializers.SerializerMethodField()

    class Meta:
        model = endpoint_models.EndpointDetail
        fields = ['headers', 'body', 'query_params', 'expiration_time_left']
        read_only_fields =  ['headers', 'query_params']

    def validate(self, attrs):
        validated_data = super().validate(attrs)
        url = self.context.get('kwargs')
        endpoint = endpoint_models.Endpoint.objects.filter(url=url, is_expired=False).first()
        if not endpoint:
            raise serializers.ValidationError('Invalid Url')
        request = self.context.get('request')
        if request and hasattr(request, 'data'):
            validated_data['body'] = dict(request.data)
        validated_data['endpoint'] = endpoint
        validated_data['headers'] = self.context.get('headers')
        validated_data['query_params'] = dict(self.context.get('query_params'))
        return validated_data

    def get_expiration_time_left(self, instance):
        time_left = (
            endpoint_constants.EXPIRATION_TIME_IN_SECONDS - (
                timezone.now() - instance.endpoint.created_at
            ).total_seconds()
        )
        return time_left
