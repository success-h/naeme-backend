from django.contrib import admin
from event.models import *
# Register your models here.

admin.site.register(Event)
admin.site.register(Ticket)
admin.site.register(BookedTicket)
admin.site.register(FAQ)
admin.site.register(EventCategory)