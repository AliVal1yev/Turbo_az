from django.shortcuts import render, redirect, get_object_or_404
from django.http import HttpResponse
from django.template import loader
from .models import CarAdvertisement, CarImage
from .forms import AdvertisementForm, AdvertisementImageFormSet, SignupForm, LoginForm
from django.conf import settings
from django.contrib import messages
from django.core.mail import send_mail
from django.contrib.auth import authenticate, login, logout
from django.contrib.auth.decorators import login_required




def user_signup(request):
    if request.method == 'POST':
        form = SignupForm(request.POST)
        if form.is_valid():
            form.save()
            return redirect('login')
    else:
        form = SignupForm()
    return render(request, 'advertisement/signup.html', {'form': form})



def user_login(request):
    if request.method == 'POST':
        form = LoginForm(request.POST)
        if form.is_valid():
            username = form.cleaned_data['username']
            password = form.cleaned_data['password']
            user = authenticate(request, username=username, password=password)
            if user:
                login(request, user)    
                return redirect('home')
    else:
        form = LoginForm()
    return render(request, 'advertisement/login.html', {'form': form})



def user_logout(request):
    logout(request)
    return redirect('cars')


def cars(request):
    ad_cars = CarAdvertisement.objects.order_by('-created_at')
    cars_with_images = []

    for car in ad_cars:
        first_image = car.images.first()
        cars_with_images.append({
            'car': car,
            'first_image': first_image
        })
    context = {
        'cars_with_images': cars_with_images
    }
    return render(request, 'advertisement/cars.html', context)


@login_required
def delete_car(request, id):
    ad = get_object_or_404(CarAdvertisement, id=id)
    
    if request.method == 'POST':
        ad.delete()
        messages.success(request, 'Advertisement deleted successfully.')
        return redirect('cars')
    
    context = {
        'ad': ad
    }
    return render(request, 'advertisement/confirm_delete.html', context)



def car_details(request, id):
  ad_cars = get_object_or_404(CarAdvertisement, id=id)
  # car_images = CarImage.objects.filter(car=ad_cars)
  # first_image = car_images.first()
  context = {
      'ad_cars': ad_cars,
      # 'car_images': car_images,
      # 'first_image': first_image,
       }

  return render(request, 'advertisement/details.html', context )


def home(request):
  return render(request, 'advertisement/home.html')

def about(request):
  return render(request, 'advertisement/about.html')

def contact(request):
  return render(request, 'advertisement/contact.html')


@login_required
def add_advertisement(request):
    if request.method == 'POST':
        form = AdvertisementForm(request.POST, request.FILES)
        formset = AdvertisementImageFormSet(request.POST, request.FILES, queryset=CarImage.objects.none())

        if form.is_valid() and formset.is_valid():
            advertisement = form.save()
            recipient = form.cleaned_data.get('your_email')
            for form in formset.cleaned_data:
                if form:
                    image = form['image']
                    CarImage.objects.create(car=advertisement, image=image)
            if recipient:
                success, message = mail_message(recipient)
                if success:
                    messages.success(request, message)
                else:
                    messages.error(request, message)
            return redirect('cars') 
    else:
        form = AdvertisementForm()
        formset = AdvertisementImageFormSet(queryset=CarImage.objects.none())

    context = {
        'form': form,
        'formset': formset,
    }
    return render(request, 'advertisement/new_ad.html', context)



def mail_message(email):
  subject = 'Confirmation'
  message = 'Your advertisement was added successfully'
  send_mail(
      subject,
      message,
      settings.EMAIL_HOST_USER,
      [email],
      fail_silently=False
  )
  return True, 'Email sent successfully!'