import json

from django.core.serializers.json import DjangoJSONEncoder
from django.shortcuts import render
from django.views.decorators.csrf import csrf_exempt
from rest_framework.response import Response
from rest_framework.decorators import api_view
from rest_framework.views import APIView

from util.util import Util
from .models import Weather
from .serializers import WeatherSerializer
import requests
import datetime

@csrf_exempt
def home(request):
    if request.method == 'POST':
        city = request.POST.get('city', 'indore')

        data = Util.get_weather_data(city)
        if data:
            if 'weather' in data and 'main' in data:
                description = data['weather'][0]['description']
                temp = data['main']['temp']
                icon = data['weather'][0]['icon']
                day = datetime.date.today()

                search_items = Util.get_city_image(city)
                image_url = search_items['items'][0]['link'] if search_items and 'items' in search_items else None

                context = {
                    'description': description,
                    'icon': icon,
                    'temp': temp,
                    'day': day,
                    'city': city,
                    'image_url': image_url,
                    'exception_occurred': False
                }
            else:
                context = {
                    'description': 'N/A',
                    'icon': 'N/A',
                    'temp': 'N/A',
                    'day': datetime.date.today(),
                    'city': city,
                    'image_url': None,
                    'exception_occurred': True
                }
        else:
            context = {
                'description': 'N/A',
                'icon': 'N/A',
                'temp': 'N/A',
                'day': datetime.date.today(),
                'city': city,
                'image_url': None,
                'exception_occurred': True
            }

        return render(request, 'index.html', context)

    return render(request, 'index.html', {
        'description': '',
        'icon': '',
        'temp': '',
        'day': datetime.date.today(),
        'city': '',
        'image_url': None,
        'exception_occurred': False
    })


class WeatherList(APIView):
    def get(self, request):
        weathers = Weather.objects.all()
        serializer = WeatherSerializer(weathers, many=True)
        return Response(serializer.data)

    def post(self, request):
        resp = {
            "success": True, "data": {
                "temperature": 0.0,
                "date": "",
                "image_url": ""
            }
        }
        city = request.data['city']
        db_item = Weather.objects.filter(city=city).first()

        if not db_item:
            data = Util.get_weather_data(city)
            description = data['weather'][0]['description']
            temp = data['main']['temp']
            db_item = Weather.objects.create(city=city, temperature=temp, description=description, date=datetime.datetime.now())
        if db_item:
            resp['data']['temperature'] = db_item.temperature
            resp['data']['date'] = db_item.date
            image = Util.get_city_image(city)
            resp['data']['image_url'] = image['items'][0]['link'] if 'items' in image else None
        resp = json.dumps(resp, ensure_ascii=False, cls=DjangoJSONEncoder)
        print(resp)
        return Response(resp)
