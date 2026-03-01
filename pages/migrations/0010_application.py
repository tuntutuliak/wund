# Application model for "Leave application" form

from django.db import migrations, models


class Migration(migrations.Migration):

    dependencies = [
        ("pages", "0009_alter_subscriber_confirmation_token"),
    ]

    operations = [
        migrations.CreateModel(
            name="Application",
            fields=[
                ("id", models.BigAutoField(auto_created=True, primary_key=True, serialize=False, verbose_name="ID")),
                ("name", models.CharField(max_length=255, verbose_name="Имя")),
                ("phone", models.CharField(max_length=20, verbose_name="Телефон")),
                ("email", models.EmailField(max_length=254, verbose_name="E-mail")),
                ("message", models.TextField(blank=True, verbose_name="Сообщение")),
                ("created_at", models.DateTimeField(auto_now_add=True, verbose_name="Дата создания")),
            ],
            options={
                "verbose_name": "Заявка",
                "verbose_name_plural": "Заявки",
                "ordering": ["-created_at"],
            },
        ),
    ]
