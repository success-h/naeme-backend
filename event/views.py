from rest_framework.response import Response
from rest_framework import status
from rest_framework import pagination

from event.pagination import CustomPagination
from .models import Ticket, Event, BookedTicket, FAQ, EventCategory
from .serializers import EventSerializer, FAQSerializer, BookedTicket, TicketSerializer, BookedTicketSerializer,  EventCategorySerializer
from rest_framework.permissions import IsAuthenticatedOrReadOnly,  AllowAny
from rest_framework import viewsets
from django_filters import rest_framework as filters


class EventFilter(filters.FilterSet):
    title = filters.CharFilter(lookup_expr='icontains') 
    class Meta:
        model = Event
        fields = ('title', "featured", "owner", "category")

class BookedTicketFilter(filters.FilterSet):
    title = filters.CharFilter(lookup_expr='icontains')
    permisson_classes = [IsAuthenticatedOrReadOnly]
    class Meta:
        model = BookedTicket
        fields = ('id', 'user', 'transactionId', 'booking_id')

class TicketFilter(filters.FilterSet):
    title = filters.CharFilter(lookup_expr='icontains')
    class Meta:
        model = Ticket
        fields = ('id', 'event',)
         


class EventList(viewsets.ModelViewSet):
    permisson_classes = [IsAuthenticatedOrReadOnly]
    pagination_class = CustomPagination
    serializer_class = EventSerializer
    queryset = Event.objects.all()
    filterset_class = EventFilter


class FAQViewSet(viewsets.ModelViewSet):
    permisson_classes = [IsAuthenticatedOrReadOnly]
    serializer_class = FAQSerializer
    queryset = FAQ.objects.all()
    
class CategoryViewSet(viewsets.ModelViewSet):
    permisson_classes = [IsAuthenticatedOrReadOnly]
    serializer_class = EventCategorySerializer
    queryset = EventCategory.objects.all()
 
         

class TicketViewSet(viewsets.ModelViewSet):
    permisson_classes = [IsAuthenticatedOrReadOnly]
    lookup_field = 'id'
    serializer_class = TicketSerializer
    queryset = Ticket.objects.all()
    filterset_class = TicketFilter


class BookedTicketViewSet(viewsets.ModelViewSet):
    permisson_classes = [IsAuthenticatedOrReadOnly]
    lookup_field = 'id'
    serializer_class = BookedTicketSerializer
    queryset = BookedTicket.objects.all()
    filterset_class = BookedTicketFilter

 