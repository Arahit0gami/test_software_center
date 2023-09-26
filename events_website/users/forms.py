from django.contrib.auth.forms import UserCreationForm, AuthenticationForm
from django.core.exceptions import ValidationError

from users.models import User


class UserRegisterForm(UserCreationForm):

    class Meta:
        model = User
        fields = [
            'login', 'first_name', 'last_name', 'date_of_birth',
        ]

    def clean_username(self):
        """Reject usernames that differ only in case."""
        login = self.cleaned_data.get("login")
        if (
            login
            and self._meta.model.objects.filter(username__iexact=login).exists()
        ):
            self._update_errors(
                ValidationError(
                    {
                        "login": self.instance.unique_error_message(
                            self._meta.model, ["login"]
                        )
                    }
                )
            )
        else:
            return login


class UserLoginForm(AuthenticationForm):

    def __init__(self, *args, **kwargs):

        """
        Обновление стилей формы регистрации
        """

        super().__init__(*args, **kwargs)

        for field in self.fields:
            self.fields['username'].widget.attrs['placeholder'] = 'Логин пользователя'
            self.fields['password'].widget.attrs['placeholder'] = 'Пароль пользователя'
            self.fields['username'].label = 'Логин'
            self.fields[field].widget.attrs.update({
                'class': 'form-control',
                'autocomplete': 'off'
            })
