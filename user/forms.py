from django import forms
from django.contrib.auth import get_user_model


class LoginForm(forms.ModelForm):
    class Meta:
        model = get_user_model()
        fields = ('username', 'password')
        widgets = {'password': forms.PasswordInput}

    def errors(self):
        errors: dict = super().errors()
        if 'username' in errors:
            username_errors = errors['username']
            for error_instance in username_errors:
                if str(error_instance)=="Пользователь с таким именем уже существует":
                    username_errors.remove(error_instance)
        return errors
