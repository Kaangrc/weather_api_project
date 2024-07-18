# create a static util class
# My module
import requests


class Util(object):

    @staticmethod
    def get_city_image(city: str) -> dict:
        API_KEY = 'AIzaSyBuxPy1Mt214HkZv8uM7IqXizsf6N-pvWU'
        SEARCH_ENGINE_ID = '408e42f7c44ad4dca'
        query = city + " 1920x1080"
        start = 1
        searchType = 'image'
        city_url = f"https://www.googleapis.com/customsearch/v1?key={API_KEY}&cx={SEARCH_ENGINE_ID}&q={query}&start={start}&searchType={searchType}&imgSize=xlarge"

        data = requests.get(city_url).json()
        print('data', data)
        return data

    @staticmethod
    def get_weather_data(city: str) -> dict:
        data = {}
        url = f'https://api.openweathermap.org/data/2.5/weather?q={city}&appid=a9158339ce8f5f746abcb808c7198977'
        PARAMS = {'units': 'metric'}

        response = requests.get(url, params=PARAMS)
        if response.status_code == 200:
            data = response.json()
        return data