from django.contrib import admin
from django.urls import path

from voucher_fulfilment import views
from voucher_fulfilment.views import booking_view

urlpatterns = [
    path("admin/", admin.site.urls),
    path('booking/', booking_view, name='booking_form'),
    path('stripe-webhook/', views.stripe_webhook, name='stripe-webhook'),

]
