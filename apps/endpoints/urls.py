from django.urls import path

from apps.endpoints import views as endpoint_views


urlpatterns = [
    path('endpoint/', endpoint_views.EndpointView.as_view()),
    path('endpointDetail/<slug:url>/', endpoint_views.EndPointDetailView.as_view()),
]
