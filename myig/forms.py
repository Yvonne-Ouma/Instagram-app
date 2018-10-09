from django import forms
from django.contrib.auth.forms import UserCreationForm
from django.contrib.auth.models import User
from .models import Profile, Image, Comment


class SignupForm(UserCreationForm):
    email = forms.EmailField(max_length=200, help_text='Required')

    class Meta:
        model = User
        fields = ('username', 'email', 'password1', 'password2')


class ProfileForm(forms.ModelForm):
    class Meta:
        model = Profile
        fields = ['user_name', 'bio', 'profile_image']


class PostForm(forms.ModelForm):
    class Meta:
        model = Image
        exclude = ['creator', 'likes', 'time', 'tags', 'comment', 'profile']


class CommentForm(forms.ModelForm):
    class Meta:
        model = Comment
        fields = ['text']
