from django.db import migrations, models


class Migration(migrations.Migration):

    dependencies = [
        ("pages", "0012_alter_groupcourserequest_preferred_start_date"),
    ]

    operations = [
        migrations.AlterField(
            model_name="groupcourserequest",
            name="email",
            field=models.EmailField(blank=True, max_length=254, verbose_name="Email"),
        ),
    ]
