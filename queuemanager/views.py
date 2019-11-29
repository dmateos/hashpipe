from django.views import View
from django.views.generic import ListView
from django.http import StreamingHttpResponse, HttpResponseNotFound
from .models import Endpoint
import time


class EndpointView(View):
    def get(self, request, id):
        endpoint = Endpoint.objects.filter(ep_id=id).first()
        if endpoint:
            return StreamingHttpResponse(endpoint.pull())
        else:
            return HttpResponseNotFound()

    def post(self, request, endpoint_id):
        pass


class EndpointList(ListView):
    model = Endpoint
    template_name = "endpoint/list.html"
    query_set = Endpoint.objects.all()
