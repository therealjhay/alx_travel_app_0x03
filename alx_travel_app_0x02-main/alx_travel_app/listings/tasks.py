from celery import shared_task
from django.core.mail import send_mail
from django.conf import settings
from .models import Payment

@shared_task
def send_payment_confirmation_email(payment_id):
    """
    Sends a confirmation email to the user after a successful payment.
    """
    try:
        payment = Payment.objects.get(id=payment_id)
        booking = payment.booking
        user_email = booking.guest_email
        subject = 'Payment Confirmation - ALX Travel App'
        message = f"""
        Dear {booking.guest_name},

        Thank you for your payment!
        
        Booking Reference: {booking.id}
        Transaction ID: {payment.transaction_id}
        Amount Paid: {payment.amount} {payment.currency}
        
        We look forward to hosting you.
        
        Best regards,
        ALX Travel Team
        """
        
        send_mail(
            subject,
            message,
            settings.EMAIL_HOST_USER,
            [user_email],
            fail_silently=False,
        )
        return f"Email sent to {user_email}"
        
    except Payment.DoesNotExist:
        return f"Payment with ID {payment_id} not found."
    except Exception as e:
        return f"Failed to send email: {str(e)}"