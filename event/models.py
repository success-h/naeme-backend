import os
from django.db import models
from django.utils import timezone
from django.contrib.auth import get_user_model
import qrcode
from io import BytesIO
from django.core.files import File
import uuid


 

User = get_user_model()

class EventCategory(models.Model):
    name = models.CharField(max_length=100)
    id = models.UUIDField(primary_key=True, default=uuid.uuid4, editable=False)

    def __str__(self):
        return self.name

class FAQ(models.Model):
    question= models.CharField(max_length=255, null=True, blank=True)
    answer = models.CharField(max_length=255, null=True, blank=True)
    id = models.UUIDField(primary_key=True, default=uuid.uuid4, editable=False)
    
    
class Event(models.Model):
    owner = models.ForeignKey(User, on_delete=models.CASCADE)
    organizer = models.CharField(max_length=255, default='Naeme') 
    title = models.CharField(max_length=200)
    description = models.CharField(max_length=5000, blank=True, null=True)
    terms = models.CharField(max_length=5000, blank=True, null=True)
    category = models.CharField(max_length=100, blank=True, null=True)
    country = models.CharField(max_length=200, default="Nigeria")
    event_faq = models.ManyToManyField(FAQ, blank=True)
    state = models.CharField(max_length=200, default="Lagos")
    city = models.CharField(max_length=200,default="Lekki")
    venue = models.CharField(max_length=200, default="Mainland bridge")
    image = models.ImageField(upload_to='event_images', blank=True, null=True)
    start_date = models.DateField(default=timezone.now)
    end_date = models.DateField(default=timezone.now)
    start_time = models.TimeField(default=timezone.now)
    end_time = models.TimeField(default=timezone.now)
    featured = models.BooleanField(default=False)
    website = models.CharField(max_length=2000,blank=True, null=True)
    created_at = models.DateTimeField(auto_now_add=True)
    qr_code = models.ImageField(upload_to='qr_codes', blank=True, null=True)
    id = models.UUIDField(primary_key=True, default=uuid.uuid4, editable=False)
    
    def get_fields(self):
        fields = super().get_fields()
        fields['event_faq'].read_only = False
        return fields

    def __str__(self):
        return self.title

    def generate_qr_code(self, *args, **kwargs):
        qrcode_img = qrcode.make(f"{os.getenv('FRONTEND_URL')}/event/{self.id}".format(self.id))
        qr_buffer = BytesIO()
        qrcode_img.save(
            qr_buffer, 
            format='PNG', 
        )
        qr_buffer.seek(0)
        self.qr_code = File(qr_buffer, name='qr_code.png')
        super().save(*args, **kwargs)
        return self.qr_code
 

    def save(self, *args, **kwargs):
        
        super().save(*args, **kwargs)

        
class Ticket(models.Model):
    title = models.CharField(max_length=200, blank=True, null=True)
    event = models.ForeignKey('Event', on_delete=models.CASCADE, related_name='tickets')
    quantity = models.IntegerField(default=0)
    price = models.IntegerField(default=0, blank=True, null=True)
    is_paid = models.BooleanField(default=False)
    id = models.UUIDField(primary_key=True, default=uuid.uuid4, editable=False) 
     
    def __str__(self):
        return  self.title



class BookedTicket(models.Model):
    event = models.ForeignKey(Event, on_delete=models.CASCADE, related_name='paid_tickets')
    ticket = models.ForeignKey(Ticket, related_name='paid_ticket', on_delete=models.CASCADE)
    user = models.ForeignKey(User, related_name='ticket_user', on_delete=models.DO_NOTHING, null=True, blank=True)
    quantity = models.IntegerField(default=0) 
    created_at = models.DateTimeField(auto_now_add=True)
    transactionId = models.CharField(max_length=200, blank=True, null=True)
    used = models.BooleanField(default=False)
    qr_code = models.ImageField(upload_to='qr_codes', blank=True, null=True)
    id = models.UUIDField(primary_key=True, default=uuid.uuid4, editable=False)
    email = models.EmailField(null=True, blank=True)
    booking_id = models.CharField(max_length=200, default=uuid.uuid4) 
    
    def __str__(self):
        return self.ticket.title

    def generate_qr_code(self, *args, **kwargs):
        qrcode_img = qrcode.make(f"{self.id}".format(self.id))
        qr_buffer = BytesIO()
        qrcode_img.save(
            qr_buffer, 
            format='PNG', 
        )
        qr_buffer.seek(0)
        self.qr_code = File(qr_buffer, name='qr_code.png')
        super().save(*args, **kwargs)
        return self.qr_code
 

    def save(self, *args, **kwargs):
        super().save(*args, **kwargs)

    


