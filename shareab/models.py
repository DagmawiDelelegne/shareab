from django.db import models
from django.contrib.auth.models import User
from .choices import CAMPUS_CHOICES
from django.core.validators import MinValueValidator
from django.core.validators import MaxLengthValidator

# Create your models here.

class Profile(models.Model):
    campus = models.CharField(max_length=10, choices=CAMPUS_CHOICES)
    user = models.OneToOneField(User,on_delete=models.CASCADE)
    social_media_link = models.CharField(max_length = 255, blank = False, null = False)
    profile_image = models.ImageField(upload_to='profile_picture/',null=True,blank=True)
    add_book = models.ManyToManyField('Book', related_name='added_by_user', blank=True)
    
    

class Book(models.Model):
    title = models.CharField(max_length=255)
    author = models.CharField(max_length=255)
    course = models.CharField(max_length=255)
    user = models.ForeignKey(User, on_delete=models.CASCADE)
    created_at = models.DateTimeField(auto_now_add=True)
    edition = models.IntegerField(validators=[MinValueValidator(1)])
    image = models.ImageField(upload_to='media/book_cover/',null=True,blank=True)

    
    class Meta:
        verbose_name = "Book"
        verbose_name_plural = "Books"

    def __str__(self):
        return self.title
