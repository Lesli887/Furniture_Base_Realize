from django import forms
from django.contrib.auth.forms import UserCreationForm, AuthenticationForm
from django.contrib.auth import get_user_model
from .models import Profile

User = get_user_model()


class RegistrationForm(UserCreationForm):
    email = forms.EmailField(
        required=True,
        widget=forms.EmailInput(attrs={'placeholder': 'example@mail.com'})
    )
    first_name = forms.CharField(required=True)
    last_name = forms.CharField(required=True)
    phone = forms.CharField(required=True)

    class Meta:
        model = User
        fields = ['email', 'first_name', 'last_name', 'phone', 'password1', 'password2']


class LoginForm(AuthenticationForm):
    username = forms.CharField(label='Email')

    def __init__(self, *args, **kwargs):
        super().__init__(*args, **kwargs)
        self.fields.pop('remember_me', None)  # Удаляем поле "Запомнить меня"


class UserForm(forms.ModelForm):
    email = forms.EmailField(
        disabled=True,
        widget=forms.EmailInput(attrs={'readonly': 'readonly'})
    )

    class Meta:
        model = User
        fields = ['first_name', 'last_name', 'email', 'phone']
        labels = {
            'first_name': 'Имя',
            'last_name': 'Фамилия',
            'email': 'Email',
            'phone': 'Телефон'
        }
        widgets = {
            'phone': forms.TextInput(attrs={'placeholder': '+7 (999) 999-99-99'})
        }


class ProfileForm(forms.ModelForm):
    class Meta:
        model = Profile
        fields = ['avatar', 'birth_date']
        labels = {
            'avatar': 'Аватар профиля',
            'birth_date': 'Дата рождения'
        }
        widgets = {
            'birth_date': forms.DateInput(
                attrs={
                    'type': 'date',
                    'max': '2010-12-31'
                },
                format='%Y-%m-%d'
            )
        }