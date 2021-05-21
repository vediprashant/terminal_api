from django.contrib import admin

from apps.endpoints import models as endpoint_models


class EndpointAdmin(admin.ModelAdmin):
    readonly_fields=('url',)

admin.site.register(endpoint_models.Endpoint, EndpointAdmin)
admin.site.register(endpoint_models.EndpointDetail)
