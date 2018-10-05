from django.shortcuts import render
import datetime as dt
from .models import Image,Profile
# Create your views here.
def welcome(request):
    date = dt.date.today()
    images = Image.objects.all()
    profiles = Profile.objects.all()
    return render(request, 'index.html',{"date": date, "images": images, "profiles": profiles})

