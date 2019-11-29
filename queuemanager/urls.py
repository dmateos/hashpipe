from django.urls import path
from . import views


urlpatterns = [
    path("ep/<slug:id>", views.EndpointView.as_view(), name="endpoint"),
    path("ep/", views.EndpointList.as_view(), name="endpoint_list"),
]
