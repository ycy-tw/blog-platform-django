from django.core.exceptions import ValidationError
from django import forms
from django.utils.translation import gettext_lazy as _
from .models import Account
from article.models import Post
from django.contrib.auth import (
    authenticate,
    password_validation,
)
from django.contrib.auth.forms import (
    UserCreationForm,
    PasswordResetForm,
    SetPasswordForm,
)


class CustomSetPasswordForm(SetPasswordForm):
    error_messages = {
        'password_mismatch': _('Two passwords didn’t match.'),
    }
    new_password1 = forms.CharField(
        label=_('New password'),
        widget=forms.PasswordInput(attrs={'class': 'client-info', }),
        strip=False,
        help_text=password_validation.password_validators_help_text_html(),
    )

    new_password2 = forms.CharField(
        label=_('Password confirmation'),
        strip=False,
        widget=forms.PasswordInput(attrs={'class': 'client-info', }),
    )


class CustomPasswordResetForm(PasswordResetForm):
    email = forms.EmailField(
        label=_('Email'),
        max_length=254,
        widget=forms.EmailInput(
            attrs={
                'class': 'client-info',
                'autocomplete': 'off',
            }),
        help_text=_('You will receive password reset link.'),
    )


class LogInForm(forms.ModelForm):
    '''
    help_text : explanation or hint for input
    '''
    email = forms.EmailField(
        label=_('Email'),
        error_messages={'required': _('Please enter email')},
        widget=forms.EmailInput(
            attrs={
                'class': 'client-info',
                'autocomplete': 'off',
            }),
    )
    password = forms.CharField(
        label=_('Password'),
        error_messages={'required': _('Please enter password')},
        widget=forms.PasswordInput(
            attrs={
                'class': 'client-info',
                'autocomplete': 'off',
            }),
    )

    class Meta:
        model = Account
        fields = ('email', 'password')

    def clean(self):
        if self.is_valid():

            email = self.cleaned_data['email']
            password = self.cleaned_data['password']

            if not authenticate(email=email, password=password):
                raise forms.ValidationError(_('Login failed, check email and password.'))


class RegistrationForm(UserCreationForm):

    '''A form for creating new users. Includes all the required
    fields, plus a repeated password.'''

    email = forms.EmailField(
        label=_('Email'),
        widget=forms.TextInput(
            attrs={
                'class': 'client-info',
                'autocomplete': 'off',
            }),
    )

    name = forms.CharField(
        label=_('Name'),
        widget=forms.TextInput(
            attrs={
                'class': 'client-info',
                'autocomplete': 'off',
            }),
    )

    password1 = forms.CharField(
        label=_('Password'),
        widget=forms.PasswordInput(attrs={
            'class': 'client-info',
            'autocomplete': 'off',
        }),
    )

    password2 = forms.CharField(
        label=_('Password confirmation'),
        widget=forms.PasswordInput(attrs={
            'class': 'client-info',
            'autocomplete': 'off',
        }),
    )

    class Meta:
        model = Account
        fields = ('email', 'name', 'password1', 'password2')

    def clean_email(self):
        email = self.cleaned_data.get('email')
        if Account.objects.filter(email=email).exists():
            raise ValidationError(_('Email already existed.'))
        return email

    def clean_password2(self):

        # Check that two passwords entries matched.
        password1 = self.cleaned_data.get('password1')
        password2 = self.cleaned_data.get('password2')
        if password1 and password2 and password1 != password2:
            raise ValidationError(_('Two passwords didn’t match.'))
        return password2

    def save(self, commit=True):

        # Save the provided password in hashed format
        user = super().save(commit=False)
        user.set_password(self.cleaned_data['password1'])
        if commit:
            user.save()
        return user


class UserEditForm(forms.ModelForm):

    class Meta:
        model = Account
        fields = ('name', 'intro', 'profile_img')
        widgets = {
            'profile_img': forms.FileInput(attrs={'class': '', 'style': 'visibility:hidden;'}),
            'name': forms.TextInput(attrs={'class': 'form-control', 'autocomplete': 'off', }),
            'intro': forms.Textarea(attrs={'class': 'form-control', 'autocomplete': 'off', }),
        }
