from django.contrib.auth.forms import UserCreationForm, AuthenticationForm, PasswordResetForm, SetPasswordForm

from catalog.forms import StyleFormMixin
from users.models import User


class StylePasswordResetMixin:
    """
   Обновление стилей форм восстановления пароля
    """
    def __init__(self, *args, **kwargs):
        super().__init__(*args, **kwargs)
        for field in self.fields:
            self.fields[field].widget.attrs.update({
                'class': 'form-control mt-2',
                'autocomplete': 'off'
            })


class UserLoginForm(StyleFormMixin, AuthenticationForm):
    """
    Форма авторизации на сайте
    """
    pass


class UserRegisterForm(StyleFormMixin, UserCreationForm):
    """
    Форма регистрации на сайте
    """

    class Meta:
        model = User
        fields = ('email', 'password1', 'password2',)


class UserForgotPasswordForm(StylePasswordResetMixin, PasswordResetForm):
    """
    Запрос на восстановление пароля
    """
    pass


class UserSetNewPasswordForm(StylePasswordResetMixin, SetPasswordForm):
    """
    Изменение пароля пользователя после подтверждения
    """
    pass
