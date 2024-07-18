# admin.py
from django.contrib import admin
from .models import Voucher


@admin.register(Voucher)
class VoucherAdmin(admin.ModelAdmin):
    list_display = (
    'code', 'product_name', 'quantity', 'total_amount', 'currency', 'customer_email', 'created_at', 'is_redeemed')
    list_filter = ('is_redeemed', 'created_at')
    search_fields = ('code', 'customer_email', 'product_name')
    readonly_fields = ('created_at',)

    fieldsets = (
        (None, {
            'fields': ('code', 'product_name', 'quantity', 'total_amount', 'currency', 'customer_email')
        }),
        ('Redemption Info', {
            'fields': ('is_redeemed', 'redeemed_at')
        }),
        ('Timestamps', {
            'fields': ('created_at',)
        }),
    )

    def has_delete_permission(self, request, obj=None):
        return False  # Prevent deletion of vouchers