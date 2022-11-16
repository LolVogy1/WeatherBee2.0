from django.shortcuts import render
from django.contrib import admin
import requests
from .models import City
from .forms import CityForm

# Create your views here.
def index(request):
    url = 'http://api.openweathermap.org/data/2.5/weather?q={}&units=imperial&appid=d0fd9eef0d6167ee1789498f1bb4ccfb'
    cities = City.objects.all() #get all cities from database

    if request.method == 'POST': #only true if form is submitted
        form = CityForm(request.POST) #add request data to form for processing
        form.save()
        
    form = CityForm()

    weather_data = []
    for city in cities:
        city_weather = requests.get(url.format(city)).json() #request API data and convert from json

        weather = {
            'city':city,
            'temperature':city_weather['main']['temp'],
            'description':city_weather['weather'][0]['description'],
            'icon':city_weather['weather'][0]['icon']
        }
        weather_data.append(weather)

    context = {'weather_data':weather_data, 'form':form}
    return render(request, 'weather/index.html', context) #returns index template