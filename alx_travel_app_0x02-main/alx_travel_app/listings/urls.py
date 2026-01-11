from django.urls import path, include
from rest_framework.routers import DefaultRouter
from .views import InitiatePaymentView, VerifyPaymentView
# from .views import ListingViewSet, BookingViewSet # <--- Uncomment if you have these ViewSets

router = DefaultRouter()
# router.register(r'listings', ListingViewSet) # <--- Uncomment if you have these ViewSets
# router.register(r'bookings', BookingViewSet) # <--- Uncomment if you have these ViewSets

urlpatterns = [
    path('', include(router.urls)),
    
    # Payment Routes
    path('payments/initiate/', InitiatePaymentView.as_view(), name='initiate-payment'),
    path('payments/verify/<str:tx_ref>/', VerifyPaymentView.as_view(), name='verify-payment'),
]