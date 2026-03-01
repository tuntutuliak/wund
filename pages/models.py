from django.db import models
from django.urls import reverse


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


class News(models.Model):
    title = models.CharField(max_length=255)
    slug = models.SlugField(max_length=255, unique=True)
    short_description = models.CharField(max_length=500, blank=True)
    content = models.TextField(blank=True)
    image = models.ImageField(upload_to="news_images/", blank=True, null=True)
    created_at = models.DateTimeField(auto_now_add=True)
    is_published = models.BooleanField(default=False)

    class Meta:
        verbose_name = "Новость"
        verbose_name_plural = "Новости"
        ordering = ["-created_at"]

    def __str__(self):
        return self.title

    def get_absolute_url(self):
        return reverse("news_detail", kwargs={"slug": self.slug})

    @property
    def image_url(self):
        """URL изображения для шаблонов: загруженный файл (media) или None (подставьте static в шаблоне)."""
        if self.image:
            return self.image.url
        return None


class Teacher(models.Model):
    full_name = models.CharField("ФИО", max_length=255)
    subject = models.CharField("Предмет / направление", max_length=255, blank=True)
    photo = models.ImageField("Фото", upload_to="teachers/", blank=True, null=True)
    is_active = models.BooleanField("Показывать в каталоге", default=True)

    class Meta:
        verbose_name = "Преподаватель"
        verbose_name_plural = "Преподаватели"
        ordering = ["full_name"]

    def __str__(self):
        return self.full_name


class EducationSection(models.Model):
    """Раздел страницы «Сведения об образовательной организации»."""
    title = models.CharField("Название", max_length=255)
    slug = models.SlugField("Якорь (slug)", max_length=255, unique=True)
    order = models.PositiveIntegerField("Порядок", default=0)
    content = models.TextField("Содержимое (HTML)", blank=True)
    is_active = models.BooleanField("Показывать на странице", default=True)

    class Meta:
        verbose_name = "Раздел (сведения)"
        verbose_name_plural = "Разделы (сведения об организации)"
        ordering = ["order"]

    def __str__(self):
        return self.title
