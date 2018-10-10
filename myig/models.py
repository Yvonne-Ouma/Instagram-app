from django.db import models
import datetime as dt
from django.contrib.auth.models import User
# Create your models here.


class Profile(models.Model):
    user = models.OneToOneField(User, on_delete=models.CASCADE)
    user_name = models.CharField(max_length=50)
    bio = models.CharField(max_length=50)
    profile_image = models.ImageField(upload_to='profiles/', blank=True)

    @classmethod
    def get_by_id(cls, id):
        profile = Profile.objects.get(user=id)
        return profile

    @classmethod
    def filter_by_id(cls, id):
        profile = Profile.objects.filter(user=id).first()
        return profile

    def save_profile(self):
        self.save()

    def delete_profile(self):
        self.delete()

    def __str__(self):
        return self.user_name


class Image(models.Model):
    name = models.CharField(max_length=20)
    image_caption = models.CharField(max_length=50)
    image = models.ImageField(upload_to='images/', blank=True)
    profile = models.ForeignKey(Profile)
    posted_time = models.DateTimeField(auto_now_add=True)

    # def save_image():
    #     self.save()

    # def delete_image():
    #     self.delete()
    @classmethod
    def filter_by_search_term(cls, search_term):
        return cls.objects.filter(image_caption__icontains=search_term)

    # @classmethod
    # def get_profile_images(cls, profile):
    #     images = Image.objects.filter(profile__pk=profile)
    #     return images

    def __str__(self):
        return self.name


class Comment(models.Model):

    text = models.CharField(max_length=200, blank=True)
    poster = models.ForeignKey(User,  on_delete=models.CASCADE)
    post = models.ForeignKey(
        Image, on_delete=models.CASCADE, related_name='comments')
    posted_time = models.DateTimeField(auto_now_add=True)

    def save_comment(self):
        self.save()

    def delete_comment(self):
        self.delete()

    def __str__(self):
        return self.text
