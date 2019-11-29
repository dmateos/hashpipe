from django.views import View
from django.views.generic import ListView
from django.http import StreamingHttpResponse, HttpResponseNotFound, HttpResponse
from .models import Endpoint
import time


class EndpointView(View):
    def get(self, request, id):
        endpoint = Endpoint.objects.filter(ep_id=id).first()
        if endpoint:
            return StreamingHttpResponse(endpoint.pull())
        else:
            return HttpResponseNotFound()

    def post(self, request, id):
        endpoint = Endpoint.objects.filter(ep_id=id).first()
        if endpoint:
            data = request.POST.get("data", False)
            if data:
                endpoint.push(data)
                return HttpResponse("ok")
        return HttpResponseNotFound()


class EndpointList(ListView):
    model = Endpoint
    template_name = "endpoint/list.html"
    query_set = Endpoint.objects.all()
