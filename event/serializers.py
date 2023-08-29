
from .models import FAQ, Event, BookedTicket,Ticket, EventCategory
from rest_framework import  serializers
from django.core.files import File
from django.db.models import Sum



class BookedTicketSerializer(serializers.ModelSerializer):

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

    start_date = serializers.SerializerMethodField(
        method_name='get_start_date',
    ) 
    
    end_date = serializers.SerializerMethodField(
        method_name='get_end_date',
    )    
    end_time = serializers.SerializerMethodField(
        method_name='get_end_time',
    )  
     
    price = serializers.SerializerMethodField(
        method_name='get_price',
    ) 
 

    class Meta:
        model = BookedTicket
        fields = ["title", "event_name", "end_date", "ticket_admin", "event", "start_date", "end_time", "email", "booking_id", "start_time", "price", "ticket", "user", "used", "quantity", "transactionId", "id", "qr_code" ]

    def get_start_date(self, instance):
        if not instance.event:
            instance.event = self.ticket.event.id
            print("hello:", self)
        return instance.ticket.event.start_date
    
    def get_end_date(self, instance):
        if not instance.event:
            instance.event = self.ticket.event.id
            print("hello:", self)
        return instance.ticket.event.end_date

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
    
    available_tickets = serializers.SerializerMethodField(
        method_name='get_available_tickets',
        read_only=True,
    )


  
    class Meta:
        model = Ticket
        fields = ["id", "price", "lowest_price", "highest_price", "title", "quantity", "available_tickets", "event", "owner", "is_paid"]
        # depth = 1

    def get_lowest_price(self, instance):
        return instance.event.tickets.order_by('price').first().price
    
    def get_highest_price(self, instance):
        return instance.event.tickets.order_by('-price').first().price

    def get_owner(self, instance):
        return instance.event.owner.id
    
    def get_available_tickets(self, instance):
        booked_tickets = BookedTicket.objects.filter(ticket=instance, used=False)
        booked_quantity_sum = booked_tickets.aggregate(Sum('quantity'))['quantity__sum']
        booked_quantity_sum = booked_quantity_sum or 0  
        available_quantity = instance.quantity - booked_quantity_sum
        return max(available_quantity, 0)   
    
    
class EventCategorySerializer(serializers.ModelSerializer):
    class Meta:
        model = EventCategory
        fields = '__all__'

class FAQSerializer(serializers.ModelSerializer):
    class Meta:
        model = FAQ
        fields = '__all__'

 
class EventSerializer(serializers.ModelSerializer): 
    event_faq = FAQSerializer(many=True, read_only=False, required=False)
    tickets = TicketSerializer(
        many=True,
        read_only=True,
    )

    paid_tickets = BookedTicketSerializer(
        many=True,
        read_only=True,
    )

    lowest_price = serializers.SerializerMethodField(
        method_name='get_lowest_price',
    )
    
    is_paid = serializers.SerializerMethodField(
        method_name='get_is_paid',
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
            "is_paid",
            "category",
            "featured",
            "country",
            "state",
            "city",
            "venue",
            "event_faq", 
            "start_date",
            "end_date",
            "start_time",
            "end_time",
            "website",
            "owner",
            "organizer",
            "qr_code",
            "terms"
        ]
        # depth = 1

    def get_lowest_price(self, instance):
        if not instance.qr_code:
            instance.generate_qr_code()
        if instance.tickets.exists():
            return instance.tickets.order_by('price').first().price 
    
    def get_highest_price(self, obj):
        if obj.tickets.exists():
            return obj.tickets.order_by('-price').first().price
    def get_is_paid(self, instance):
        tickets = instance.tickets.all()
        for ticket in tickets:
            return ticket.is_paid



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
    
    def get_is_paid(self, obj):
        if obj.tickets.exists():
            if obj.tickets.filter(is_paid=True).exists():
                return True
            else:
                return False
    
    def create(self, validated_data):
        faq_data = validated_data.pop('event_faq', [])
        event = Event.objects.create(**validated_data)

        for faq_item in faq_data:
            faq = FAQ.objects.create(**faq_item)
            event_faq = event.event_faq  # Get the related manager
            event_faq.add(faq)

        return event
