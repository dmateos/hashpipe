from django.views import View
from django.http import StreamingHttpResponse, HttpResponseNotFound
from .models import Endpoint


class EndpointView(View):
    def get(self, request, id):
        endpoint = Endpoint.objects.filter(ep_id=id).first()
        if endpoint:
            return StreamingHttpResponse(self._data_generator())
        else:
            return HttpResponseNotFound()

    def post(self, request, endpoint_id):
        pass

    def _data_generator(self):
        yield "hello"
        yield "world"
