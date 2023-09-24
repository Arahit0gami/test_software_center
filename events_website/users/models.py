from django.contrib.auth.base_user import AbstractBaseUser
from django.contrib.auth.models import PermissionsMixin
from django.db import models
from django.utils import timezone
from django.utils.translation import gettext_lazy as _
from rest_framework.exceptions import ValidationError


class UserManager(models.Manager):
    use_in_migrations = True

    def _create_user(self, login, password, **extra_fields):
        if not login:
            raise ValueError('Поле login не может быть пустым! ')
        user = self.model(login=login, **extra_fields)
        user.set_password(password)
        user.save(using=self._db)
        return user

    def create_user(self, login, password=None, **extra_fields):
        extra_fields.setdefault('is_staff', False)
        extra_fields.setdefault('is_superuser', False)
        return self._create_user(login, password, **extra_fields)

    def create_superuser(self, login, password=None, **extra_fields):
        extra_fields.setdefault('is_staff', True)
        extra_fields.setdefault('is_superuser', True)

        if extra_fields.get('is_staff') is not True:
            raise ValueError('Администратор должен иметь is_staff=True.')
        if extra_fields.get('is_superuser') is not True:
            raise ValueError('Администратор должен иметь is_superuser=True.')

        return self._create_user(login, password, **extra_fields)

    def get_by_natural_key(self, login):
        return self.get(**{self.model.USERNAME_FIELD: login})


class CustomUser(AbstractBaseUser, PermissionsMixin):

    id = models.AutoField(primary_key=True)
    login = models.CharField(max_length=20, unique=True)
    first_name = models.CharField(_("first name"), max_length=150)
    last_name = models.CharField(_("last name"), max_length=150)
    date_of_birth = models.DateField(blank=True, null=True)
    is_staff = models.BooleanField(
        _("staff status"),
        default=False,
        help_text=_("Designates whether the user can log into this admin site."),
    )
    is_active = models.BooleanField(
        _("active"),
        default=True,
        help_text=_(
            "Designates whether this user should be treated as active. "
            "Unselect this instead of deleting accounts."
        ),
    )
    date_joined = models.DateTimeField(_("date joined"), default=timezone.now)

    objects = UserManager()

    USERNAME_FIELD = 'login'
    REQUIRED_FIELDS = []

    def clean(self):
        super().clean()
        if self.date_of_birth and self.date_of_birth > timezone.now().date():
            raise ValidationError(
                "Дата рождения не может быть больше  текущей даты."
            )