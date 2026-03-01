# Generated manually for Subscriber model

import uuid
from django.db import migrations, models


class Migration(migrations.Migration):

    dependencies = [
        ("pages", "0007_remove_education_section"),
    ]

    operations = [
        migrations.CreateModel(
            name="Subscriber",
            fields=[
                ("id", models.BigAutoField(auto_created=True, primary_key=True, serialize=False, verbose_name="ID")),
                ("email", models.EmailField(db_index=True, max_length=254, unique=True, verbose_name="E-mail")),
                ("is_active", models.BooleanField(default=False, verbose_name="Подтверждён")),
                ("confirmation_token", models.UUIDField(default=uuid.uuid4, editable=False, unique=True)),
                ("created_at", models.DateTimeField(auto_now_add=True, verbose_name="Дата подписки")),
                ("confirmed_at", models.DateTimeField(blank=True, null=True, verbose_name="Дата подтверждения")),
                ("ip_address", models.GenericIPAddressField(blank=True, null=True, verbose_name="IP-адрес")),
                ("user_agent", models.TextField(blank=True, verbose_name="User-Agent")),
            ],
            options={
                "verbose_name": "Подписчик",
                "verbose_name_plural": "Подписчики",
                "ordering": ["-created_at"],
            },
        ),
    ]
