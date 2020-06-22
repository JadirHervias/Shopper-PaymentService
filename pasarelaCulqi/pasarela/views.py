from django.http import HttpResponse
from django.views.decorators.csrf import csrf_exempt
from rest_framework.renderers import JSONRenderer
from rest_framework.parsers import JSONParser
from .models import Pago
from .serializers import PagoSerializer
from .procesos.cargo import generar_cargo
import json

class JSONResponse(HttpResponse):
    """
    An HttpResponse that renders its content into JSON.
    """
    def __init__(self, data, **kwargs):
        content = JSONRenderer().render(data)
        kwargs['content_type'] = 'application/json'
        super(JSONResponse, self).__init__(content, **kwargs)
    
@csrf_exempt
def pago_list(request):
    """
    List all pagos, or create a new pago.
    """
    if request.method == 'GET':
        pagos = Pago.objects.all()
        serializer = PagoSerializer(pagos, many=True)
        return JSONResponse(serializer.data)

    elif request.method == 'POST':
        data = JSONParser().parse(request)
        serializer = PagoSerializer(data=data)
        if serializer.is_valid():
            serializer.save()
            rpta = generar_cargo(data=data)
            return JSONResponse(rpta, status=201)
        return JSONResponse(serializer.errors, status=400)

