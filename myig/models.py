from django.db import models
import datetime as dt
# Create your models here.

class Profile(models.Model):
    user_name = models.CharField(max_length=50)
    bio = models.CharField(max_length=50)
    profile_image = models.ImageField(upload_to = 'profiles/',blank = True)
    

    def save_profile(self):
        self.save()

    def delete_profile(self):
        self.delete() 

           
    def __str__(self):
        return self.user_name


class Image(models.Model):
    name = models.CharField(max_length=20)
    image_caption = models.CharField(max_length=50)
    image = models.ImageField(upload_to = 'images/',blank = True)
    profile = models.ForeignKey(Profile)
    posted_time = models.DateTimeField(auto_now_add=True)

    def save_image():
        self.save()

    def delete_image():
         self.delete()    
    

    def __str__(self):
        return self.name
