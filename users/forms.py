from django import forms
from django.contrib.auth import get_user_model

from django.contrib.auth.forms import UserCreationForm
from django.utils.translation import gettext_lazy as _

from .models import Feedback

User = get_user_model()


class CreationForm(UserCreationForm):
    first_name = forms.CharField(
        max_length=50,
        label=_('Ім\'я'),
        widget=forms.TextInput(attrs={'placeholder': _('Ім\'я')})
    )
    last_name = forms.CharField(
        max_length=50,
        label=_('Прізвище'),
        widget=forms.TextInput(attrs={'placeholder': _('Прізвище')})
    )
    username = forms.CharField(
        max_length=150,
        label=_('Логін'),
        widget=forms.TextInput(attrs={'placeholder': _('Логін')})
    )
    email = forms.EmailField(
        label=_('Електронна пошта'),
        widget=forms.EmailInput(attrs={'placeholder': _('Електронна пошта')}),
        required=False
    )
    password1 = forms.CharField(
        label=_('Пароль'),
        widget=forms.PasswordInput(attrs={'placeholder': _('Пароль')})
    )
    password2 = forms.CharField(
        label=_('Підтвердження пароля'),
        widget=forms.PasswordInput(attrs={'placeholder': _('Підтвердження пароля')})
    )
    phone = forms.CharField(
        max_length=13,
        label=_('Телефон'),
        widget=forms.TextInput(attrs={'placeholder': _('Телефон')})
    )




    class Meta(UserCreationForm.Meta):
        model = User
        fields = ('first_name', 'last_name', 'username', 'email', 'password1', 'password2', 'phone')
        

MESSENGER_CHOICES = [
    ('viber', 'Viber'),
    ('telegram', 'Telegram'),
    ('whatsapp', 'WhatsApp'),
]

class FeedbackForm(forms.ModelForm):
    feedback_messengers = forms.MultipleChoiceField(
        choices=MESSENGER_CHOICES,
        widget=forms.CheckboxSelectMultiple,
        required=False,
        label='Доступні месенджери',
    )

    class Meta:
        model = Feedback
        fields = ['feedback_name', 'feedback_email', 'feedback_message', 'feedback_phone', 'feedback_messengers']


