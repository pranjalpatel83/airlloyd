import logging
import uuid

import stripe
from django.conf import settings
from django.db import IntegrityError
from django.http import HttpResponse
from django.shortcuts import render, redirect
from django.views.decorators.csrf import csrf_exempt
from django.views.decorators.http import require_POST

from .forms import BookingForm, PassengerFormSet
from .models import Passenger
from .models import Voucher
from .utils import send_voucher_email

logger = logging.getLogger(__name__)

stripe.api_key = settings.STRIPE_SECRET_KEY


def booking_view(request):
    if request.method == 'POST':
        booking_form = BookingForm(request.POST)
        passenger_formset = PassengerFormSet(request.POST, request.FILES)
        if booking_form.is_valid() and passenger_formset.is_valid():
            booking = booking_form.save()
            passengers = passenger_formset.save(commit=False)
            if len(passengers) > 3:
                booking_form.add_error(None, "You can add a maximum of 3 passengers.")
            else:
                for passenger in passengers:
                    passenger.booking = booking
                    passenger.save()
                passenger_formset.save_m2m()
                return redirect('booking_success')  # Redirect to a success page or another page
    else:
        booking_form = BookingForm()
        passenger_formset = PassengerFormSet()

    return render(request, 'booking.html', {
        'booking_form': booking_form,
        'passenger_formset': passenger_formset,
    })

@csrf_exempt
@require_POST
def stripe_webhook(request):
    payload = request.body
    sig_header = request.META['HTTP_STRIPE_SIGNATURE']

    try:
        event = stripe.Webhook.construct_event(
            payload, sig_header, settings.STRIPE_WEBHOOK_SECRET
        )
    except ValueError as e:
        logger.error(f"Invalid payload: {str(e)}")
        return HttpResponse(status=400)
    except stripe.error.SignatureVerificationError as e:
        logger.error(f"Invalid signature: {str(e)}")
        return HttpResponse(status=400)

    if event['type'] == 'checkout.session.completed':
        session = event['data']['object']

        try:
            handle_successful_payment(session)
        except Exception as e:
            logger.error(f"Error handling successful payment: {str(e)}")
            return HttpResponse(status=500)

    return HttpResponse(status=200)


def handle_successful_payment(session):
    logger.info(f"Processing successful payment for session: {session['id']}")

    try:
        customer_email = get_customer_email(session)
        if not customer_email:
            logger.error(f"Unable to retrieve customer email for session: {session['id']}")
            return

        line_items = stripe.checkout.Session.list_line_items(session['id'], limit=1)

        if not line_items.data:
            logger.error(f"No line items found for session: {session['id']}")
            return

        item = line_items.data[0]
        product_name = item['description']
        quantity = item['quantity']
        total_amount = session['amount_total'] / 100
        currency = session['currency']

        voucher = generate_voucher(product_name, quantity, total_amount, currency, customer_email)
        send_voucher_email(voucher)
        logger.info(f"Voucher {voucher.code} sent to {customer_email}")
    except Exception as e:
        logger.error(f"Error in voucher generation or sending: {str(e)}")
        raise


def get_customer_email(session):
    # Check customer_details first
    if session.get('customer_details') and session['customer_details'].get('email'):
        return session['customer_details']['email']

    # Then check customer_email
    if session.get('customer_email'):
        return session['customer_email']

    # If still no email, check if it's available in the customer object
    if session.get('customer'):
        try:
            customer = stripe.Customer.retrieve(session['customer'])
            return customer.get('email')
        except stripe.error.StripeError as e:
            logger.error(f"Error retrieving customer: {str(e)}")

    return None


def generate_voucher(product_name, quantity, total_amount, currency, customer_email):
    prefix = "VCH-"
    for _ in range(5):  # Try up to 5 times
        code = f"{prefix}{uuid.uuid4().hex[:8].upper()}"
        try:
            voucher = Voucher.objects.create(
                code=code,
                product_name=product_name,
                quantity=quantity,
                total_amount=total_amount,
                currency=currency,
                customer_email=customer_email
            )
            return voucher
        except IntegrityError:
            continue
    raise Exception("Failed to generate a unique voucher code after multiple attempts")
