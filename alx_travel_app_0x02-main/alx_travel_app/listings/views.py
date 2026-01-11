import requests
import uuid
import os
from rest_framework.views import APIView
from rest_framework.response import Response
from rest_framework import status
from django.shortcuts import get_object_or_404
from .models import Booking, Payment
from .serializers import PaymentSerializer
from .tasks import send_payment_confirmation_email

class InitiatePaymentView(APIView):
    def post(self, request, *args, **kwargs):
        # 1. Get the booking ID from the request
        booking_id = request.data.get('booking_id')
        if not booking_id:
            return Response({"error": "booking_id is required"}, status=status.HTTP_400_BAD_REQUEST)

        booking = get_object_or_404(Booking, id=booking_id)

        # 2. Generate unique info
        tx_ref = str(uuid.uuid4()) # Unique Transaction Reference
        amount = str(booking.listing.price) 
        currency = "ETB"
        email = booking.guest_email
        first_name = booking.guest_name.split()[0] if booking.guest_name else "Guest"
        
        # 3. Construct the payload for Chapa
        # Note: We use os.environ.get to read the key from your .env file
        payload = {
            "amount": amount,
            "currency": currency,
            "email": email,
            "first_name": first_name,
            "tx_ref": tx_ref,
            # In a real app, callback_url is your webhook. return_url is where the user goes after paying.
            "return_url": f"http://127.0.0.1:8000/api/payments/verify/{tx_ref}/" 
        }

        headers = {
            'Authorization': f'Bearer {os.environ.get("CHAPA_SECRET_KEY")}',
            'Content-Type': 'application/json'
        }

        # 4. Send Request to Chapa
        chapa_url = "https://api.chapa.co/v1/transaction/initialize"
        try:
            response = requests.post(chapa_url, json=payload, headers=headers)
            data = response.json()

            if response.status_code == 200 and data['status'] == 'success':
                # 5. Save Payment Record LOCALLY as 'Pending'
                Payment.objects.create(
                    booking=booking,
                    transaction_id=tx_ref,
                    amount=booking.listing.price,
                    currency=currency,
                    status='Pending'
                )
                
                # Return the checkout URL to the frontend so the user can pay
                return Response({
                    "checkout_url": data['data']['checkout_url'],
                    "tx_ref": tx_ref
                }, status=status.HTTP_200_OK)
            else:
                return Response({"error": "Failed to initialize payment", "details": data}, status=status.HTTP_400_BAD_REQUEST)

        except requests.exceptions.RequestException as e:
            return Response({"error": str(e)}, status=status.HTTP_503_SERVICE_UNAVAILABLE)


class VerifyPaymentView(APIView):
    def get(self, request, tx_ref, *args, **kwargs):
        # 1. Find the local payment record
        payment = get_object_or_404(Payment, transaction_id=tx_ref)

        headers = {
            'Authorization': f'Bearer {os.environ.get("CHAPA_SECRET_KEY")}',
        }

        # 2. Ask Chapa for the official status
        verify_url = f"https://api.chapa.co/v1/transaction/verify/{tx_ref}"
        
        try:
            response = requests.get(verify_url, headers=headers)
            data = response.json()

            if response.status_code == 200 and data['status'] == 'success':
                # 3. Update Status to Completed
                payment.status = 'Completed'
                payment.save()
                
                # TODO: We will add the email notification here in the next step
                
                return Response({"message": "Payment verified successfully", "data": data}, status=status.HTTP_200_OK)
            else:
                # Update Status to Failed
                payment.status = 'Failed'
                payment.save()
                return Response({"message": "Payment verification failed", "data": data}, status=status.HTTP_400_BAD_REQUEST)

        except requests.exceptions.RequestException as e:
            return Response({"error": str(e)}, status=status.HTTP_503_SERVICE_UNAVAILABLE)