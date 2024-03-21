from django import forms
from artecho.models import Image, Category, UserProfile
from django.contrib.auth.forms import AuthenticationForm
from django.contrib.auth.models import User

class LoginForm(AuthenticationForm):
    password = forms.CharField(widget=forms.PasswordInput())
    username = forms.CharField(help_text="")
    class Meta:
        model = UserProfile
        fields = ('username', 'password',)

class UserForm(forms.ModelForm):
    password = forms.CharField(widget=forms.PasswordInput())
    username = forms.CharField(help_text="")
    class Meta:
        model = User
        fields = ('username', 'email', 'password',)
class UserProfileForm(forms.ModelForm):
    class Meta:
        model = UserProfile
        fields = ( )

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

class ImageForm(forms.ModelForm):
    category = forms.ModelChoiceField(queryset=Category.objects.all(), empty_label="Select a category")
    class Meta:
        model = Image
        fields = ('name', 'isAI', 'category', 'description', 'file' )
        labels = {
            'isAI': 'Is this image AI generated?',
        }

class ProfileForm(forms.ModelForm):
    class Meta:
        model = UserProfile
        fields = ['bio', 'profilePicture' ]
        labels = {
            'totalLikes': 'Total Likes',
            'profilePicture': 'Profile Picture',
        }
class UserForm(forms.ModelForm):
    def clean_username(self):
        username = self.cleaned_data.get('username')
        return username
    password = forms.CharField(widget=forms.PasswordInput())
    class Meta:
        model = User
        fields = ('username', 'email', 'password',)
    
class UserProfileForm(forms.ModelForm):
     class Meta:
        model = UserProfile
        fields = [ ] 
        labels = {
            'totalLikes': 'Total Likes',
        }