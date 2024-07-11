from django.shortcuts import render, redirect, get_object_or_404
from .models import CarAdvertisement, CarImage
from .forms import AdvertisementForm, AdvertisementImageFormSet, SignupForm, LoginForm, CarFilterForm
from django.contrib import messages
from django.contrib.auth import authenticate, login, logout
from django.contrib.auth.decorators import login_required
from django.http import JsonResponse
from django.views.decorators.csrf import csrf_exempt
from .tasks import send_confirmation_mail_task, send_deleted_mail_task, send_update_notification_task

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
        if car.car_status == "APPROVE":
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
        if ad.user == request.user:
            ad.car_status = ad.REJECTED
            ad.save()
            send_deleted_mail_task(ad.id)
            
        else:
            return render(request, 'advertisement/delete_message.html')
        messages.success(request, 'Advertisement deleted successfully.')
        return redirect('cars')
    context = {
        'ad': ad
    }
   
    return render(request, 'advertisement/confirm_delete.html', context)



def car_details(request, id):
  ad_cars = get_object_or_404(CarAdvertisement, id=id)
  context = {
      'ad_cars': ad_cars,
       }

  return render(request, 'advertisement/details.html', context )



def home(request):
    ad_cars = CarAdvertisement.objects.order_by('-created_at')
    cars_with_images = []
    for car in ad_cars:
        if car.car_status == "APPROVE" and car.vip_car:
            first_image = car.images.first()
            cars_with_images.append({
                'car': car,
                'first_image': first_image
            })
    context = {
        'cars_with_images': cars_with_images
    }
    return render(request, 'advertisement/home.html', context)


def filter(request):
    form = CarFilterForm(request.GET)
    advertisements = CarAdvertisement.objects.order_by('-created_at')
    cars_with_images = []
    if form.is_valid():
        name = form.cleaned_data.get('car_brand')
        model = form.cleaned_data.get('car_model')
        category = form.cleaned_data.get('category')
        fuel_type = form.cleaned_data.get('fuel_type')
        if name:
            advertisements = advertisements.filter(name=name)
        if model:
            advertisements = advertisements.filter(model=model)
        if category:
            advertisements = advertisements.filter(category=category)
        if fuel_type:
            advertisements = advertisements.filter(fuel_type=fuel_type)
        for car in advertisements:
            if car.car_status == "APPROVE":
                first_image = car.images.first()
                cars_with_images.append({
                    'car': car,
                    'first_image': first_image
                })
        context = {
            'form': form,
            'cars_with_images': cars_with_images
        }
    return render(request, 'advertisement/filter.html', context)



def about(request):
  return render(request, 'advertisement/about.html')


@login_required
def add_advertisement(request):
    if request.method == 'POST':
        form = AdvertisementForm(request.POST, request.FILES)
        formset = AdvertisementImageFormSet(request.POST, request.FILES, queryset=CarImage.objects.none())

        if form.is_valid() and formset.is_valid():
            advertisement = form.save(commit=False)
            advertisement.user = request.user 
            advertisement.save()
            send_confirmation_mail_task.delay(advertisement.id)
            for form in formset.cleaned_data:
                if form:
                    image = form['image']
                    CarImage.objects.create(car=advertisement, image=image)
                    
            return redirect('cars') 
    else:
        form = AdvertisementForm()
        formset = AdvertisementImageFormSet(queryset=CarImage.objects.none())

    context = {
        'form': form,
        'formset': formset,
    }
    return render(request, 'advertisement/new_ad.html', context)


@login_required
def my_cars(request):
    cars = CarAdvertisement.objects.filter(user=request.user).order_by('-created_at')
    cars_with_images = []

    for car in cars:
        if car.car_status == car.APPROVE:
            first_image = car.images.first()
            cars_with_images.append({
                'car': car,
                'first_image': first_image
            })
    context = {
        'cars_with_images': cars_with_images
    }
    return render(request, 'advertisement/my_advertisement.html', context)
    


@csrf_exempt
def toggle_favorite(request, ad_id):
    ad = get_object_or_404(CarAdvertisement, id=ad_id)
    if request.user in ad.favorites.all():
        ad.favorites.remove(request.user)
        status = 'removed'
    else:
        ad.favorites.add(request.user)
        status = 'added'
    return JsonResponse({'status': status, 'ad_id': ad_id})

@login_required
def favorite_cars(request):
    cars_with_images = []
    cars = CarAdvertisement.objects.filter(favorites=request.user).order_by('-created_at')
    for car in cars:
        if car.car_status == car.APPROVE:
            first_image = car.images.first()
            cars_with_images.append({
                'car': car,
                'first_image': first_image
            })
    context = {
        'cars_with_images': cars_with_images
    }
    return render(request, 'advertisement/favorites.html', context)


@login_required
def edit_car(request, pk):
    advertisement = get_object_or_404(CarAdvertisement, pk=pk)
    if request.user != advertisement.user:
        return redirect('cars') 
    if request.method == 'POST':
        form = AdvertisementForm(request.POST, request.FILES, instance=advertisement)
        formset = AdvertisementImageFormSet(request.POST, request.FILES, queryset=CarImage.objects.filter(car=advertisement))
        if form.is_valid() and formset.is_valid():
            advertisement = form.save(commit=False)
            advertisement.user = request.user
            advertisement.save()
            send_update_notification_task(advertisement.id)
            CarImage.objects.filter(car=advertisement).delete()
            for form in formset.cleaned_data:
                if form:
                    image = form['image']
                    CarImage.objects.create(car=advertisement, image=image)
            return redirect('cars')
    else:
        form = AdvertisementForm(instance=advertisement)
        formset = AdvertisementImageFormSet(queryset=CarImage.objects.filter(car=advertisement))

    context = {
        'form': form,
        'formset': formset,
    }
    return render(request, 'advertisement/edit.html', context)