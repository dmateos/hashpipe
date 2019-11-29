from django.urls import path
from . import views


urlpatterns = [
    path("ep/create", views.EndpointCreate.as_view(), name="endpoint_create"),
    path("ep/<slug:id>", views.EndpointView.as_view(), name="endpoint"),
    path("ep/<int:pk>/edit", views.EndpointUpdate.as_view(), name="endpoint_edit"),
    path("ep/", views.EndpointList.as_view(), name="endpoint_list"),
]
