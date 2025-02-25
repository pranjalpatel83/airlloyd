# Generated by Django 5.0.7 on 2024-07-10 21:33

from django.db import migrations, models


class Migration(migrations.Migration):

    initial = True

    dependencies = []

    operations = [
        migrations.CreateModel(
            name="Voucher",
            fields=[
                (
                    "id",
                    models.BigAutoField(
                        auto_created=True,
                        primary_key=True,
                        serialize=False,
                        verbose_name="ID",
                    ),
                ),
                ("code", models.CharField(max_length=50, unique=True)),
                ("created_at", models.DateTimeField(auto_now_add=True)),
                ("redeemed_at", models.DateTimeField(blank=True, null=True)),
                ("is_redeemed", models.BooleanField(default=False)),
                ("product_name", models.CharField(max_length=255)),
                ("quantity", models.PositiveIntegerField()),
                ("total_amount", models.DecimalField(decimal_places=2, max_digits=10)),
                ("currency", models.CharField(max_length=3)),
                ("customer_email", models.EmailField(max_length=254)),
            ],
        ),
    ]
