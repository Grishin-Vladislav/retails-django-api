from rest_framework.response import Response
from rest_framework.views import APIView

from .serializers import HelloWorldSerializer


class HelloWorldView(APIView):
    def get(self, request, *args, **kwargs):
        message = 'Hello world'
        serializer = HelloWorldSerializer({'message': message})
        return Response(serializer.data)
