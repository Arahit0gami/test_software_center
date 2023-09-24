from django.conf import settings
from django.db import models
from django.utils import timezone
from rest_framework.exceptions import ValidationError


class Event(models.Model):
    objects = models.Manager()

    title = models.CharField(max_length=150)
    text = models.CharField(max_length=1000)
    date_event = models.DateTimeField()
    date_create = models.DateTimeField(default=timezone.now)
    author = models.ForeignKey(
        settings.AUTH_USER_MODEL,
        on_delete=models.PROTECT,
        related_name='author'
    )
    participants = models.ManyToManyField(
        settings.AUTH_USER_MODEL,
        related_name='participants'
    )

    def clean(self):
        super().clean()
        if self.date_event < timezone.now():
            raise ValidationError(
                "Дата события не может быть меньше текущей даты."
            )
