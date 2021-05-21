from celery.utils.log import get_task_logger
from celery import task

from apps.endpoints import (
    models as endpoint_models,
    utils as endpoint_utils
)

logger = get_task_logger(__name__)


@task()
def delete_expired_urls():
    """
    Task to delete all expired Url's
    """
    logger.info('Url Deletion Task Started')
    endpoint_utils.update_expiration_field()
    endpoint_models.Endpoint.objects.filter(is_expired=True).delete()
    logger.info('Url Deletion Task Finished')
