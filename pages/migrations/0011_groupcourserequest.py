from django.db import migrations, models


class Migration(migrations.Migration):

    dependencies = [
        ("pages", "0010_application"),
    ]

    operations = [
        migrations.CreateModel(
            name="GroupCourseRequest",
            fields=[
                ("id", models.BigAutoField(auto_created=True, primary_key=True, serialize=False, verbose_name="ID")),
                ("preferred_start_date", models.CharField(blank=True, max_length=100)),
                ("group_type", models.CharField(choices=[("mini", "Mini-group (up to 6 students)"), ("standard", "Standard group"), ("intensive", "Intensive")], max_length=20)),
                ("level", models.CharField(choices=[("beginner", "Beginner"), ("intermediate", "Intermediate"), ("advanced", "Advanced")], max_length=20)),
                ("schedule", models.CharField(choices=[("2_per_week", "2 times per week"), ("3_per_week", "3 times per week"), ("daily", "Intensive (daily)")], max_length=20)),
                ("name", models.CharField(max_length=150)),
                ("phone", models.CharField(max_length=50)),
                ("email", models.EmailField(max_length=254)),
                ("created_at", models.DateTimeField(auto_now_add=True)),
                ("processed", models.BooleanField(default=False)),
            ],
            options={
                "ordering": ["-created_at"],
            },
        ),
    ]
