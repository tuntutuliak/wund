from django.db import models


class Course(models.Model):
    title = models.CharField(max_length=255)
    slug = models.SlugField(max_length=255, unique=True)
    subtitle = models.CharField(max_length=500, blank=True)
    image = models.FileField(upload_to="courses/", blank=True, null=True)
    description = models.TextField(blank=True)
    teacher = models.CharField(max_length=255, blank=True)
    start_date = models.DateField(null=True, blank=True)
    duration = models.CharField(max_length=100, blank=True)
    price = models.CharField(max_length=100, blank=True)

    class Meta:
        verbose_name = "Курс"
        verbose_name_plural = "Курсы"

    def __str__(self):
        return self.title
