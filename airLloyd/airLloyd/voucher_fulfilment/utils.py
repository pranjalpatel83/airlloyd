# utils.py
from django.core.mail import send_mail
from django.template.loader import render_to_string
from django.conf import settings


def send_voucher_email(voucher):
    subject = f'Your Voucher for {voucher.product_name}'
    context = {
        'voucher': voucher,
    }
    html_message = render_to_string('emails/voucher_email.html', context)
    plain_message = render_to_string('emails/voucher_email.txt', context)

    send_mail(
        subject,
        plain_message,
        settings.DEFAULT_FROM_EMAIL,
        [voucher.customer_email],
        html_message=html_message,
        fail_silently=False,
    )