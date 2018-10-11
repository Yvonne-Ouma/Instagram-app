from django.http import HttpResponse
from django.shortcuts import render, redirect, get_object_or_404
import datetime as dt
from .models import Image, Profile
from django.contrib.auth.decorators import login_required
from django.contrib.auth import login, authenticate
from .forms import SignupForm, ProfileForm, PostForm, CommentForm
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
    profiles = Profile.objects.all()
    return render(request, 'index.html', {"date": date, "images": images, 'profiles': profiles})


def signup(request):
    if request.method == 'POST':
        form = SignupForm(request.POST)
        if form.is_valid():
            user = form.save(commit=False)
            user.is_active = False
            user.save()
            profile=Profile(user=user)
            profile.save()
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
        return HttpResponse('Thank you for your email confirmation. Now you can login your account.')
    else:
        return HttpResponse('Activation link is invalid!')


@login_required(login_url='/accounts/login/')
def search_results(request):
    if 'search' in request.GET and request.GET["search"]:
        search_term = request.GET.get('search')
        photos = Image.filter_by_search_term(search_term)
        print(photos)
        message = f"{search_term}"

    # else:
    #     message = "No searched profile"
    #     return render(request, 'search.html', {"message": message})
    return render(request, 'search.html', {"message": message, "photos": photos})


@login_required(login_url='/accounts/login/')
def profile(request):
    current_user = request.user
    user = User.objects.get(username=request.user)
    profile = Profile.objects.get(user=current_user)
    # try:
    #     profile = Profile.get_by_id(profile.id)
    # except:
    #     profile = Profile.filter_by_id(profile.id)
    # images = Image.get_profile_images(profile.id)
    return render(request, 'profile/profile.html', {'user': current_user, "profile":profile})


@login_required(login_url='/accounts/login/')
def edit_profile(request):
    form = ProfileForm()
    user = request.user
    if request.user.is_authenticated():
        if request.method == "POST":
            try:
                profile = user.profile
                form = ProfileForm(instance=profile)
                form = ProfileForm(
                    request.POST, request.FILES, instance=profile)
                if form.is_valid():
                    update = form.save(commit=False)
                    update.user = user
                    update.save()
            except:
                form = ProfileForm(request.POST, request.FILES)
                print(form.is_valid())
                if form.is_valid():
                    form.save()
                    user_name = form.cleaned_data['user_name']
                    profile = Profile.objects.get(user_name=user_name)
                    print(profile)
                    profile.user = user
                    profile.save()
            return redirect('welcome')
    else:
        form = ProfileForm()

    return render(request, 'profile/edit_profile.html', {'form': form, 'user': user})


@login_required(login_url='/accounts/login/')
def post_image(request):
    if request.method == 'POST':
        form = PostForm(request.POST, request.FILES)
        if form.is_valid():
            post = form.save(commit=False)
            post.profile = request.user.profile
            post.save()
            return redirect('welcome')

    else:
        form = PostForm()
        return render(request, 'post_photo.html', {"form": form})


@login_required(login_url='/accounts/login/')
def comment(request, id):
    image = get_object_or_404(Image, pk=id)
    current_user = request.user
    if request.method == 'POST':
        form = CommentForm(request.POST)
        if form.is_valid():
            comment = form.save(commit=False)
            comment.post = image
            comment.poster = current_user
            comment.save()
            return redirect('welcome')
    else:
        form = CommentForm()
    return render(request, 'comment.html', {"form": form})
