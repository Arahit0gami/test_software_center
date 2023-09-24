from django.conf import settings
from django.contrib import admin
from django.utils.translation import gettext_lazy as _


from .models import CustomUser


@admin.register(CustomUser)
class CustomUserAdmin(admin.ModelAdmin):
    model = settings.AUTH_USER_MODEL
    list_display = [
        'id', 'first_name', 'last_name', 'date_of_birth',
        'date_joined', 'is_active', 'is_staff', 'is_superuser'
    ]
    search_fields = ("login", "first_name", "last_name", "email")
    ordering = ('login',)

    fieldsets = (
        (None, {"fields": ("login", "password")}),
        (_("Personal info"), {
            "fields": ("first_name", "last_name", "date_of_birth")
        }),
        (
            _("Permissions"),
            {
                "fields": (
                    "is_active",
                    "is_staff",
                    "is_superuser",
                    "groups",
                    "user_permissions",
                ),
            },
        ),
        (_("Important dates"), {"fields": ("last_login", "date_joined")}),
    )
    add_fieldsets = (
        (
            None,
            {
                "classes": ("wide",),
                "fields": (
                    "login", "password1", "password2",
                    "first_name", "last_name", "date_of_birth"
                ),
            },
        ),
    )