# models.py

from django.db import models


class Booking(models.Model):
    LOCATION_CHOICES = [
        ('Bonn-Hangelar', 'Bonn-Hangelar'),
        ('Ganderkesee', 'Ganderkesee'),
    ]
    DURATION_CHOICES = [
        ('30', '30 Minuten'),
        ('45', '45 Minuten'),
        ('60', '60 Minuten'),
    ]
    TIME_SLOT_CHOICES = [
        ('09:00', '09:00'),
        ('11:30', '11:30'),
        ('12:30', '12:30'),
    ]
    location = models.CharField(max_length=50, choices=LOCATION_CHOICES)
    duration = models.CharField(max_length=2, choices=DURATION_CHOICES)
    date = models.DateField()
    time_slot = models.CharField(max_length=5, choices=TIME_SLOT_CHOICES)
    created_at = models.DateTimeField(auto_now_add=True)


class Passenger(models.Model):
    SALUTATION_CHOICES = [
        ('Herr', 'Herr'),
        ('Frau', 'Frau'),
    ]
    salutation = models.CharField(max_length=10, choices=SALUTATION_CHOICES)
    first_name = models.CharField(max_length=100)
    last_name = models.CharField(max_length=100)
    weight = models.DecimalField(max_digits=5, decimal_places=2)
    phone = models.CharField(max_length=20)
    email = models.EmailField()
    ticket_number = models.CharField(max_length=20)
    booking = models.ForeignKey(Booking, related_name='passengers', on_delete=models.CASCADE)


class Voucher(models.Model):
    code = models.CharField(max_length=50, unique=True)
    created_at = models.DateTimeField(auto_now_add=True)
    redeemed_at = models.DateTimeField(null=True, blank=True)
    is_redeemed = models.BooleanField(default=False)
    product_name = models.CharField(max_length=255)
    quantity = models.PositiveIntegerField()
    total_amount = models.DecimalField(max_digits=10, decimal_places=2)
    currency = models.CharField(max_length=3)
    customer_email = models.EmailField()

    def __str__(self):
        return f"{self.code} - {self.product_name} ({self.quantity})"

    class Meta:
        ordering = ['-created_at']
