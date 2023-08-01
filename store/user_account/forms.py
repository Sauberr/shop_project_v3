import uuid
from datetime import timedelta

from captcha.fields import CaptchaField
from django import forms
from django.contrib.auth.forms import (AuthenticationForm, PasswordChangeForm,
                                       UserChangeForm, UserCreationForm)
from django.utils.timezone import now

from user_account.models import EmailVerification, User
from user_account.tasks import send_email_verification


class UserLoginForm(AuthenticationForm):
    username = forms.CharField(widget=forms.TextInput(attrs={
        'class': 'form-control py-4', 'placeholder': 'Enter username'
    }))
    password = forms.CharField(widget=forms.PasswordInput(attrs={
        'class': 'form-control py-4', 'placeholder': 'Enter password'
    }))

    class Meta:
        model = User
        fields = '__all__'


class UserRegistrationForm(UserCreationForm):
    first_name = forms.CharField(widget=forms.TextInput(attrs={
        'class': 'form-control py-2', 'placeholder': 'Enter first_name'
    }))
    last_name = forms.CharField(widget=forms.TextInput(attrs={
        'class': 'form-control py-2', 'placeholder': 'Enter last_name'
    }))
    username = forms.CharField(widget=forms.TextInput(attrs={
        'class': 'form-control py-2', 'placeholder': 'Enter username'
    }))
    email = forms.CharField(widget=forms.EmailInput(attrs={
        'class': 'form-control py-2', 'placeholder': 'Enter gmail'
    }))
    password1 = forms.CharField(widget=forms.PasswordInput(attrs={
        'class': 'form-control py-2', 'placeholder': 'Enter password'
    }))
    password2 = forms.CharField(widget=forms.PasswordInput(attrs={
        'class': 'form-control py-2', 'placeholder': 'Enter password again'
    }))
    captcha = CaptchaField()

    class Meta:
        model = User
        fields = ('first_name', 'last_name', 'username', 'email', 'password1', 'password2')

    # Email validation
    def clean_email(self):
        email = self.cleaned_data.get('email')
        if User.objects.filter(email=email).exists():
            raise forms.ValidationError('This email is invalid')
        if len(email) >= 350:
            raise forms.ValidationError('Your email is too long')

        return email

    def save(self, commit=True):
        user = super(UserRegistrationForm, self).save(commit=True)
        expiration = now() + timedelta(hours=48)
        record = EmailVerification.objects.create(code=uuid.uuid4(), user=user, expiration=expiration)
        record.send_verification_email()
        return user
        # send_email_verification.delay(user.id)
        # return user


class PasswordChangingPassword(PasswordChangeForm):

    old_password = forms.CharField(widget=forms.PasswordInput(attrs={
        'class': 'form-control py-2', 'placeholder': 'Old password' }))

    new_password1 = forms.CharField(widget=forms.PasswordInput(attrs={
        'class': 'form-control py-2', 'placeholder': 'New password' }))

    new_password2 = forms.CharField(widget=forms.PasswordInput(attrs={
        'class': 'form-control py-2', 'placeholder': 'Confirm password' }))

    class Meta:
        model = User
        fields = ('old_password', 'new_password1', 'new_password2')


class UserUpdateForm(forms.ModelForm):
    password = None

    username = forms.CharField(widget=forms.TextInput(attrs={
        'class': 'form-control py-2', 'placeholder': 'Enter username'
    }))
    email = forms.CharField(widget=forms.EmailInput(attrs={
        'class': 'form-control py-2', 'placeholder': 'Enter gmail'
    }))

    class Meta:
        model = User
        fields = ['username', 'email']
        exclude = ['password1', 'password2']

    # Email validation
    def clean_email(self):
        email = self.cleaned_data.get('email')
        if User.objects.filter(email=email).exclude(pk=self.instance.pk).exists():
            raise forms.ValidationError('This email is invalid')
        if len(email) >= 350:
            raise forms.ValidationError('Your email is too long')

        return email

    # Make fields required
    # def __init__(self, *args, **kwargs):
    #     super(UpdateUserForm, self).__init__(*args, **kwargs)
    #
    #     self.fields['email'].required = True


class UserProfileForm(UserChangeForm):
    first_name = forms.CharField(widget=forms.TextInput(attrs={
        'class': 'form-control py-2', 'placeholder': 'Enter first_name'
    }))
    last_name = forms.CharField(widget=forms.TextInput(attrs={
        'class': 'form-control py-2', 'placeholder': 'Enter last_name'
    }))
    image = forms.ImageField(widget=forms.FileInput(attrs={
        'class': 'custom-file-input',
    }), required=False)
    username = forms.CharField(widget=forms.TextInput(attrs={
        'class': 'form-control py-2', 'placeholder': 'Enter username', 'readonly': True,
    }))
    email = forms.CharField(widget=forms.EmailInput(attrs={
        'class': 'form-control py-2', 'placeholder': 'Enter gmail', 'readonly': True,
    }))

    class Meta:
        model = User
        fields = ('first_name', 'last_name', 'image', 'username', 'email')





