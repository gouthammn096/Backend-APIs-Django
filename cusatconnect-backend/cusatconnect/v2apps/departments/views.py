from rest_framework.generics import RetrieveAPIView, ListAPIView
from rest_framework.permissions import IsAuthenticated
from rest_framework import status
from rest_framework.response import Response

from .models import Stream
from .serializers import StreamSerializer


class DepView(RetrieveAPIView):

    permission_classes = ()
    serializer_class = StreamSerializer

    def get_object(self):
        return Stream.objects.get(pk=self.kwargs.get('pk'))


class StreamView(ListAPIView):

    permission_classes = ()
    serializer_class = StreamSerializer

    def get_queryset(self):
        return Stream.objects.all()
