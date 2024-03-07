from django import forms
from django.contrib.auth.models import User
from artecho.models import UserProfile

class LoginForm(forms.ModelForm):
    password = forms.CharField(widget=forms.PasswordInput())
    class Meta:
        model = User
        fields = ('email', 'password',)
class UserForm(forms.ModelForm):
    password = forms.CharField(widget=forms.PasswordInput())
    username = forms.CharField(help_text="")
    class Meta:
        model = User
        fields = ('username', 'email', 'password',)
class UserProfileForm(forms.ModelForm):
    class Meta:
        model = UserProfile
        fields = ( 'picture',)

class SignUpForm(UserForm):
    password_confirm = forms.CharField(widget=forms.PasswordInput(), label='Confirm password')

    class Meta(UserForm.Meta):
        fields = UserForm.Meta.fields + ('password_confirm',)

    def clean(self):
        cleaned_data = super().clean()
        password = cleaned_data.get('password')
        password_confirm = cleaned_data.get('password_confirm')

        if password != password_confirm:
            self.add_error('password_confirm', 'Passwords must match')

        return cleaned_data