from django.contrib import admin
from django.utils.translation import gettext_lazy as _

from events.models import Event


@admin.register(Event)
class EventAdmin(admin.ModelAdmin):
    list_display = (
        'title', 'text', 'date_event',
        'date_create',
    )
    search_fields = ("title", "text", "date_event",)
    ordering = ('-date_event',)
    list_filter = ["title", "date_event", 'date_create']
    fieldsets = (
        (_("Event main info"), {
            "fields": ("title", "text", "author")
        }),
        (
            _("Participants"),
            {
                "fields": (
                    "participants",
                ),
            },
        ),
        (_("Important dates"), {"fields": ("date_event", "date_create")}),
    )
    add_fieldsets = (
        (
            None,
            {
                "classes": ("wide",),
                "fields": (
                    'title', 'text', 'date_event',
                ),
            },
        ),
    )
