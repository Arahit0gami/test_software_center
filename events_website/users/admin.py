from django.conf import settings
from django.contrib import admin
from django.contrib.auth.admin import UserAdmin
from django.utils.translation import gettext_lazy as _

from .forms import UserRegisterForm
from .models import User


@admin.register(User)
class UserAdmin(UserAdmin):
    add_form = UserRegisterForm
    model = settings.AUTH_USER_MODEL
    list_display = [
        'id', 'first_name', 'last_name', 'date_of_birth',
        'date_joined', 'is_active', 'is_staff', 'is_superuser'
    ]
    search_fields = ("login", "first_name", "last_name", "date_of_birth")
    ordering = ('login',)
    list_filter = ["is_active", 'is_staff', "date_of_birth"]

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
