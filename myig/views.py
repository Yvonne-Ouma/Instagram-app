from django.http import HttpResponse
from django.shortcuts import render, redirect
import datetime as dt
from .models import Image, Profile
from django.contrib.auth.decorators import login_required
from django.contrib.auth import login, authenticate
from .forms import SignupForm, ProfileForm
from django.contrib.sites.shortcuts import get_current_site
from django.utils.encoding import force_bytes, force_text
from django.utils.http import urlsafe_base64_encode, urlsafe_base64_decode
from django.template.loader import render_to_string
from .tokens import account_activation_token
from django.contrib.auth.models import User
from django.core.mail import EmailMessage


# Create your views here.

@login_required(login_url='/accounts/login/')
def welcome(request):
    date = dt.date.today()
    images = Image.objects.all()
    return render(request, 'index.html', {"date": date, "images": images})


def signup(request):
    if request.method == 'POST':
        form = SignupForm(request.POST)
        if form.is_valid():
            user = form.save(commit=False)
            user.is_active = False
            user.save()
            current_site = get_current_site(request)
            mail_subject = 'Activate your blog account.'
            message = render_to_string('acc_active_email.html', {
                'user': user,
                'domain': current_site.domain,
                'uid': urlsafe_base64_encode(force_bytes(user.pk)),
                'token': account_activation_token.make_token(user),
            })
            to_email = form.cleaned_data.get('email')
            email = EmailMessage(
                mail_subject, message, to=[to_email]
            )
            email.send()
            return HttpResponse('Please confirm your email address to complete the registration')
    else:
        form = SignupForm()
    return render(request, 'signup.html', {'form': form})


def activate(request, uidb64, token):
    try:
        uid = force_text(urlsafe_base64_decode(uidb64))
        user = User.objects.get(pk=uid)
    except(TypeError, ValueError, OverflowError, User.DoesNotExist):
        user = None
    if user is not None and account_activation_token.check_token(user, token):
        user.is_active = True
        user.save()
        login(request, user)
        # return redirect('home')
        return HttpResponse('Thank you for your email confirmation. Now you can login your account.')
    else:
        return HttpResponse('Activation link is invalid!')


def search_results(request):
    if 'profile' in request.GET and request.GET["profile"]:
        search_term = request.GET.get('profile')
        searched_profiles = Profile.search_profile(search_term)
        message = f"{search_term}"

        return render(request, 'search.html', {"message": message, "profiles": searched_profiles})

    else:
        message = "No searched profile"
        return render(request, 'search.html', {"message": message})


@login_required(login_url='/accounts/login/')
def profile(request):
    profile = User.objects.get(username=request.user)
    try:
        profile = Profile.get_by_id(profile.id)
    except:
        profile = Profile.filter_by_id(profile.id)
    images = Image.get_profile_images(profile.id)
    return render(request, 'profile/profile.html', {'profile': profile, 'profile': profile, 'images': images})


@login_required(login_url='/accounts/login')
def edit_profile(request):
    if request.method == 'POST':
        form = ProfileForm(request.POST, request.FILES)
        if form.is_valid():
            edit = form.save(commit=False)
            edit.user = request.user
            edit.save()
            return redirect('edit_profile')
    else:
        form = ProfileForm()

    return render(request, 'profile/edit_profile.html', {'form': form})

# def profile(request):
#     photo = Profile.objects.all()
#     user = User.objects.get(username=request.user)
#     print(photo)

#     print('photo')
#     if request.method == 'POST':
#         form = ProfileForm(request.POST, request.FILES,
#                            instance=request.user.profile)
#         if form.is_valid():
#             form.save()
#     else:
#         form = ProfileForm()
#     return render(request, 'profile/profile.html', {"form": form, 'user': user, "photo": photo})
