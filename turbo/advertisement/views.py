from django.shortcuts import render, redirect
from django.http import HttpResponse
from django.template import loader
from .models import Advertisement
from .forms import AdvertisementForm


# def advertisement(request):
#     return HttpResponse("Hello world!")


def cars(request):
    ad_cars = Advertisement.objects.all().order_by('-created_at')
    template = loader.get_template('advertisement/cars.html')
    context = {
        'ad_cars': ad_cars
        }
    return HttpResponse(template.render(context, request))


def car_details(request, id):
  ad_cars = Advertisement.objects.get(id=id)
  template = loader.get_template('advertisement/details.html')
  context = {
    'ad_cars': ad_cars,
  }
  return HttpResponse(template.render(context, request))



def home(request):
  return render(request, 'advertisement/home.html')

def about(request):
  return render(request, 'advertisement/about.html')

def contact(request):
  return render(request, 'advertisement/contact.html')


def add_advertisement(request):
  if request.method == 'POST':
    form = AdvertisementForm(request.POST, request.FILES)
    if form.is_valid():
      form.save()
      return redirect('cars')  
    else:
        return render(request, 'advertisement/new_ad.html', {'form': form})
  else:
      form = AdvertisementForm()
  return render(request, 'advertisement/new_ad.html', {'form': form})