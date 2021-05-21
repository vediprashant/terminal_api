from datetime import timedelta

from django.utils import timezone

from apps.endpoints import (
    models as endpoint_models,
    constants as endpoint_constants
)


def update_expiration_field():
    """
    To update expired field of Endpoint if it has been expired
    """
    endpoint_models.Endpoint.objects.filter(
        created_at__lte=timezone.now() - timedelta(seconds=endpoint_constants.EXPIRATION_TIME_IN_SECONDS)
    ).update(is_expired=True)
