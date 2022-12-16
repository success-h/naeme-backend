
from event.models import *
from rest_framework import  serializers
from django.contrib.auth import get_user_model
import os
from django.core.files import File



class PaidTicketSerializer(serializers.ModelSerializer):

    title = serializers.SerializerMethodField(
        method_name='get_title',
    )   
    event_name = serializers.SerializerMethodField(
        method_name='get_event_name',
    )   
    ticket_admin = serializers.SerializerMethodField(
        method_name='get_ticket_admin',
    )   
    start_time = serializers.SerializerMethodField(
        method_name='get_start_time',
    )

    date = serializers.SerializerMethodField(
        method_name='get_date',
    )    
    end_time = serializers.SerializerMethodField(
        method_name='get_end_time',
    )  
     
    price = serializers.SerializerMethodField(
        method_name='get_price',
    ) 
 

    class Meta:
        model = PaidTicket
        fields = ["title", "event_name", "ticket_admin", "event", "date", "end_time", "start_time", "price", "ticket", "user", "used", "quantity", "transactionId", "id", "qr_code" ]

    def get_date(self, instance):
        if not instance.event:
            instance.event = self.ticket.event.id
            print("hello:", self)
        return instance.ticket.event.date

    def get_title(self, instance):
        if not instance.qr_code:
            print("[instance]:", instance)
            instance.generate_qr_code()
        return instance.ticket.title
    
    def get_end_time(self, instance):
        return instance.ticket.event.end_time

    def get_ticket_admin(self, instance):
        return instance.ticket.event.owner.id

    def get_start_time(self, instance):
        return instance.ticket.event.start_time
     
    def get_event_name(self, instance):
        return instance.ticket.event.title
    
    def get_price(self, instance):
        return instance.ticket.price 
    


class TicketSerializer(serializers.ModelSerializer):

    lowest_price = serializers.SerializerMethodField(
        method_name='get_lowest_price',
    )

    highest_price = serializers.SerializerMethodField(
        method_name='get_highest_price',
    )
    
 
    owner = serializers.SerializerMethodField(
        method_name='get_owner',
        read_only=True
    )

  
    class Meta:
        model = Ticket
        fields = ["id", "price", "lowest_price", "highest_price", "title", "quantity", "event", "owner"]
        # depth = 1

    def get_lowest_price(self, instance):
        return instance.event.tickets.order_by('price').first().price
    
    def get_highest_price(self, instance):
        return instance.event.tickets.order_by('-price').first().price

    def get_owner(self, instance):
        return instance.event.owner.id

 
class EventSerializer(serializers.ModelSerializer): 
    tickets = TicketSerializer(
        many=True,
        read_only=True,
    )

    paid_tickets = PaidTicketSerializer(
        many=True,
        read_only=True,
    )

    lowest_price = serializers.SerializerMethodField(
        method_name='get_lowest_price',
    )

    highest_price = serializers.SerializerMethodField(
        method_name='get_highest_price',
    )

    total_ticket_count = serializers.SerializerMethodField(
        method_name='get_total_ticket_quantity',
        read_only=True,
    )

    total_sold_tickets = serializers.SerializerMethodField(
        method_name='get_total_sold_tickets',
        read_only=True,
    )
         
         
    class Meta:
        model = Event
        fields = [
            "id",
            "tickets",
            "paid_tickets",
            "total_ticket_count",
            "total_sold_tickets",
            "lowest_price",
            "highest_price",
            "title",
            "description",
            "image",
            "liked",
            "featured",
            "location",
            "date",
            "start_time",
            "end_time",
            "website",
            "owner",
            "organizer",
          ]

    def get_lowest_price(self, obj):
        if obj.tickets.exists():
            return obj.tickets.order_by('price').first().price 


    def get_highest_price(self, obj):
        if obj.tickets.exists():
            return obj.tickets.order_by('-price').first().price


    def get_total_ticket_quantity(self, obj):
        if obj.tickets.exists():
            tickets = obj.tickets.all()
            quantity = 0
            for item in tickets:
                quantity += item.quantity
            return quantity
            
    def get_total_sold_tickets(self, obj):
        if obj.paid_tickets.exists():
            tickets = obj.paid_tickets.all()
            quantity = 0
            for item in tickets:
                quantity += item.quantity
            return quantity