from django.views import View
from django.views.generic import ListView, UpdateView
from django.http import StreamingHttpResponse, HttpResponseNotFound, HttpResponse
from django.views.decorators.csrf import csrf_exempt
from django.utils.decorators import method_decorator
from django.urls import reverse_lazy
from .models import Endpoint
import time


@method_decorator(csrf_exempt, name="dispatch")
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


class EndpointUpdate(UpdateView):
    model = Endpoint
    template_name = "endpoint/form.html"
    success_url = reverse_lazy("endpoint_list")
    fields = ["engine", "ep_id"]
