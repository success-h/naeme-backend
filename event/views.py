from rest_framework.response import Response
from rest_framework import status
from rest_framework import pagination

from event.pagination import CustomPagination
from .models import Ticket, Event, PaidTicket
from .serializers import *
from rest_framework.permissions import IsAuthenticatedOrReadOnly
from rest_framework import viewsets
from django_filters import rest_framework as filters


class EventFilter(filters.FilterSet):
    title = filters.CharFilter(lookup_expr='icontains') 
    class Meta:
        model = Event
        fields = ('title', "featured", "owner")

class PaidTicketFilter(filters.FilterSet):
    title = filters.CharFilter(lookup_expr='icontains')
    class Meta:
        model = PaidTicket
        fields = ('id', 'user')

class TicketFilter(filters.FilterSet):
    title = filters.CharFilter(lookup_expr='icontains')
    class Meta:
        model = Ticket
        fields = ('id', 'event')
         


class EventList(viewsets.ModelViewSet):
    permisson_classes = [IsAuthenticatedOrReadOnly]
    pagination_class = CustomPagination
    serializer_class = EventSerializer
    queryset = Event.objects.all()
    filterset_class = EventFilter

         

class TicketViewSet(viewsets.ModelViewSet):
    permisson_classes = [IsAuthenticatedOrReadOnly]
    lookup_field = 'id'
    serializer_class = TicketSerializer
    queryset = Ticket.objects.all()
    filterset_class = TicketFilter


class PaidTicketViewSet(viewsets.ModelViewSet):
    permisson_classes = [IsAuthenticatedOrReadOnly]
    lookup_field = 'id'
    serializer_class = PaidTicketSerializer
    queryset = PaidTicket.objects.all()
    filterset_class = PaidTicketFilter

 