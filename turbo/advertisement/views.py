from django.shortcuts import render
from django.http import HttpResponse
from django.template import loader
from .models import Advertisement


# def advertisement(request):
#     return HttpResponse("Hello world!")


def cars(request):
    ad_cars = Advertisement.objects.all()
    template = loader.get_template('cars.html')
    context = {
        'ad_cars': ad_cars
        }
    return HttpResponse(template.render(context, request))


def car_details(request, id):
  ad_cars = Advertisement.objects.get(id=id)
  template = loader.get_template('details.html')
  context = {
    'ad_cars': ad_cars,
  }
  return HttpResponse(template.render(context, request))



def home(request):
  return render(request, 'home.html')

def about(request):
  return render(request, 'about.html')

def contact(request):
  return render(request, 'contact.html')
