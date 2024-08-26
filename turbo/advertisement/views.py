from django.shortcuts import render, redirect, get_object_or_404
from .models import CarAdvertisement, CarImage, CarName, CarModel, Category, FuelType, User
from .forms import AdvertisementForm, AdvertisementImageFormSet, SignupForm, LoginForm, CarFilterForm, VerificationForm
from django.contrib import messages
import random
from django.contrib.auth import authenticate, login, logout
from django.contrib.auth.decorators import login_required
from django.http import JsonResponse
from django.views.decorators.csrf import csrf_exempt
from .tasks import *
from rest_framework import viewsets, status
from .serializers import CarSerializer, CarNameSerializer, CarModelSerializer, CategorySerializer, FuelTypeSerializer
from rest_framework.decorators import api_view
from rest_framework.response import Response
from rest_framework_simplejwt.tokens import RefreshToken


verification_code = random.randint(100000, 999999)


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
        verify_form = VerificationForm
        if form.is_valid():
            username = form.cleaned_data['username']
            password = form.cleaned_data['password']
            user = authenticate(request, username=username, password=password)
            user_email = user.email
            if user:
                verification_code = random.randint(100000, 999999)
                send_verify_code_mail_task.delay(user_email, verification_code)
                request.session['verification_code'] = verification_code
                request.session['username'] = username
                request.session.save()
                
                refresh = RefreshToken.for_user(user)
                access_token = str(refresh.access_token)
                
                # Store JWT in session
                request.session['jwt'] = access_token
                return redirect('verify') 
            
    else:
        form = LoginForm()
    return render(request, 'advertisement/login.html', {'form': form})


def verify_view(request):
    if request.method == 'POST':
        form = VerificationForm(request.POST)
        if form.is_valid():
            verification_code = form.cleaned_data['verification_code']
            if verification_code == str(request.session.get('verification_code')):
                username = request.session.get('username')
                user = User.objects.get(username=username)
                login(request, user)
                return redirect('home')
            else:
                form.add_error(None, 'Invalid verification code')
    else:
        form = VerificationForm()
    return render(request, 'advertisement/verify.html', {'form': form})


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
            send_deleted_mail_task.delay(ad.id)
            
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
  ad_cars.watch_count += 1
  ad_cars.save(update_fields=['watch_count'])
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


def filter_view(request):
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
def edit_car(request, ad_id):
    advertisement = get_object_or_404(CarAdvertisement, id=ad_id, user=request.user)

    if request.method == 'POST':
        form = AdvertisementForm(request.POST, request.FILES, instance=advertisement)
        formset = AdvertisementImageFormSet(request.POST, request.FILES, instance=advertisement)

        if form.is_valid() and formset.is_valid():
            if advertisement.car_status != advertisement.REJECTED:
                advertisement = form.save(commit=False)
                advertisement.user = request.user
                advertisement.car_status = advertisement.PENDING
                advertisement.save()
                send_update_notification_task.delay(advertisement.id)
                formset.save() 
                return redirect('details', ad_id)
            return redirect('details', ad_id)
    else:
        form = AdvertisementForm(instance=advertisement)
        formset = AdvertisementImageFormSet(instance=advertisement)

    context = {
        'form': form,
        'formset': formset,
        'advertisement': advertisement,
    }
    return render(request, 'advertisement/edit.html', context)



class CarAdvertisementViewSet(viewsets.ModelViewSet):
    queryset = CarAdvertisement.objects.all()
    serializer_class = CarSerializer


class CarNameViewSet(viewsets.ModelViewSet):
    queryset = CarName.objects.all()
    serializer_class = CarNameSerializer


class CarModelViewSet(viewsets.ModelViewSet):
    queryset = CarModel.objects.all()
    serializer_class = CarModelSerializer


class CategoryViewSet(viewsets.ModelViewSet):
    queryset = Category.objects.all()
    serializer_class = CategorySerializer


class FuelTypeViewSet(viewsets.ModelViewSet):
    queryset = FuelType.objects.all()
    serializer_class = FuelTypeSerializer



@api_view(['GET', 'POST', 'PUT', 'PATCH', 'DELETE'])
def carmodel_view_api(request):
    if request.method == 'GET':
        car_model = CarModel.objects.all()
        serializer = CarModelSerializer(car_model, many=True)
        return Response({ 'msg': 'Successfully retrived data', 'data':serializer.data}, status=status.HTTP_200_OK)
    
    elif request.method == 'POST':
        serializer = CarModelSerializer(data=request.data)
        if serializer.is_valid():
            serializer.save()
            return Response({'msg':'Car created successfully', 'data':serializer.data}, status=status.HTTP_201_CREATED)
        return Response(serializer.errors, status=status.HTTP_400_BAD_REQUEST)
    
    elif request.method == 'PUT':
        car_model = CarModel.objects.get(pk=request.data.get('id'))
        serializer = CarModelSerializer(car_model, data = request.data)
        if serializer.is_valid():
            serializer.save()
            return Response({'msg': 'Car model updated successfully', 'data':serializer.data}, status=status.HTTP_200_OK)
        return Response(serializer.errors, status=status.HTTP_400_BAD_REQUEST)
    
    elif request.method == 'DELETE':
        car_model = CarModel.objects.get(pk=request.data.get('id'))
        car_model.delete()
        return Response({'msg': 'Car model deleted successfully'}, status=status.HTTP_204_NO_CONTENT)
    
    return Response({'msg': 'Invalid  request method'}, status=status.HTTP_405_METHOD_NOT_ALLOWED)