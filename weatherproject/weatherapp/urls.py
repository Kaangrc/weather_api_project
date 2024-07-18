from django.contrib import admin
from django.urls import path
from weatherapp.views import home, WeatherList

urlpatterns = [
    path('admin/', admin.site.urls),
    path('', home, name='home'),  # HTML sayfasını render eden yol
    path('api/weather/', WeatherList.as_view(), name='weather-list'),  # REST API için yol
]
