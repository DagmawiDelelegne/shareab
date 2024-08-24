from django.contrib.auth.forms import UserCreationForm,AuthenticationForm
from django.contrib.auth.models import User

from django import forms 
from .models import Book, Profile
from .choices import CAMPUS_CHOICES
from django.forms.widgets import PasswordInput, TextInput

class CreateUserForm(UserCreationForm):
    campus = forms.ChoiceField(choices=CAMPUS_CHOICES, required=True)
    social_media_link = forms.CharField(max_length= 255,label="Social Medial or Email", required=True)
    profile_image = forms.ImageField(required=False)

    class Meta:
        model = User
        fields = ['username', 'password1', 'password2', 'campus', 'social_media_link', 'profile_image']

# - login a user
        
class LoginForm(AuthenticationForm):
        username = forms.CharField(widget=TextInput())
        password = forms.CharField(widget=PasswordInput())

# - search bar
class BookSearchForm(forms.Form):
     search_query = forms.CharField(label="Enter title of the book", max_length= 100)

# - add a book
class BookForm(forms.ModelForm):
    title = forms.CharField(
        max_length=255,
        label="Title:",
        widget=forms.TextInput(attrs={'class': 'form-control'})
    )
    author = forms.CharField(
        max_length=255,
        label="Author:",
        widget=forms.TextInput(attrs={'class': 'form-control'})
    )
    course = forms.CharField(
        max_length=255,
        label="Course:",
        widget=forms.TextInput(attrs={'class': 'form-control'})
    )
    edition = forms.IntegerField(
        label="Edition:",
        widget=forms.NumberInput(attrs={'class': 'form-control'})
    )
    image = forms.ImageField(
        required=False,
        label="Book Cover:",
        widget=forms.ClearableFileInput(attrs={'class': 'form-control-file'})
    )
    class Meta:
        model = Book
        fields = ['title', 'author', 'course', 'edition', 'image']
        
class ProfileForm(forms.ModelForm):
    class Meta:
        model = Profile
        fields = ['campus', 'profile_image', 'social_media_link']
