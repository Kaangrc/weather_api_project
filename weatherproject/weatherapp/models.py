from django.db import models

class Weather(models.Model):
    city = models.CharField(max_length=100)
    description = models.CharField(max_length=100)
    temperature = models.FloatField()
    date = models.DateField(auto_now_add=True)

    def __str__(self):
        return f'{self.city} - {self.description} - {self.temperature}°C'
