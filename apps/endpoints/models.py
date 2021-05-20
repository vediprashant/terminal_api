import uuid

from django.db import models

from apps.commons import models as commons_models


class Endpoint(commons_models.TimeStampModel):
    """
    Model to store the details of unique url
    """
    url = models.UUIDField(default=uuid.uuid1, unique=True, editable=False)
    is_expired = models.BooleanField(default=False)

    def __str__(self):
        return '{} -> {}'.format(self.url, self.created_at)


class EndpointDetails(commons_models.TimeStampModel):
    """
    Model to store the data that is being hit to the url
    """
    endpoint = models.ForeignKey(Endpoint, to_field='url', on_delete=models.CASCADE)
    headers = models.JSONField(
        null=True, blank=True, default=dict,
        help_text='headers associated with HTTP request'
    )
    body = models.JSONField(
        null=True, blank=True, default=dict,
        help_text='Body data associated with HTTP request'
    )
    query_params = models.JSONField(
        null=True, blank=True, default=dict,
        help_text='Query parameters associated with HTTP request'
    )

    def __str__(self):
        return '{} -> {}'.format(self.endpoint.url, self.endpoint.is_expired)
