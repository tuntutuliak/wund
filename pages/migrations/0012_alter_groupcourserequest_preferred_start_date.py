from django.db import migrations, models


def clear_invalid_dates(apps, schema_editor):
    from datetime import datetime
    GroupCourseRequest = apps.get_model("pages", "GroupCourseRequest")
    for obj in GroupCourseRequest.objects.all():
        val = obj.preferred_start_date or ""
        if val == "":
            continue
        try:
            datetime.strptime(str(val)[:10], "%Y-%m-%d")
        except (ValueError, TypeError):
            obj.preferred_start_date = ""
            obj.save(update_fields=["preferred_start_date"])


def noop(apps, schema_editor):
    pass


class Migration(migrations.Migration):

    dependencies = [
        ("pages", "0011_groupcourserequest"),
    ]

    operations = [
        migrations.RunPython(clear_invalid_dates, noop),
        migrations.AlterField(
            model_name="groupcourserequest",
            name="preferred_start_date",
            field=models.DateField(blank=True, null=True, verbose_name="Желаемая дата начала"),
        ),
    ]
