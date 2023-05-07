from event.views import *
from rest_framework.routers import DefaultRouter


app_name = 'event_api'
router = DefaultRouter()
router.register('events', EventList, basename='events' )
router.register('tickets', TicketViewSet, basename='tickets')
router.register('my-tickets', PaidTicketViewSet, basename='my-tickets')
router.register('faq', FAQViewSet, basename='faq')
router.register('event-category', CategoryViewSet, basename='event-category')

urlpatterns = router.urls
