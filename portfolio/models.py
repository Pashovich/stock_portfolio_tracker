from django.db import models
from django.conf import settings
import json
import zlib

class Share(models.Model):
    name = models.CharField(max_length=255)
    price = models.DecimalField(max_digits=10, decimal_places=2)
    qty = models.IntegerField()
    date_of_purchase = models.DateField()

    def __str__(self):
        return self.name

    def set_data(self, data: dict) -> None:
        self.current_price = data.get('current_price', None)
        self.upcomming_dividents = data.get('upcomming_dividents', None)
        


class Portfolio(models.Model):
    user = models.ForeignKey(settings.AUTH_USER_MODEL, on_delete=models.CASCADE)
    name = models.CharField(max_length=255)
    shares = models.ManyToManyField(Share, blank=True)
    created_at = models.DateTimeField(auto_now_add=True)

    def __str__(self):
        return self.name
    
    def delete(self, *args, **kwargs):
    
        self.shares.all().delete()
        super().delete(*args, **kwargs)


class DividendCalculation(models.Model):
    user = models.ForeignKey(settings.AUTH_USER_MODEL, on_delete=models.CASCADE)
    ticket_name = models.CharField(max_length=255)
    capital = models.FloatField()
    lookback_period = models.CharField(max_length=255)
    calculation_period = models.CharField(max_length=255)
    created_at = models.DateTimeField(auto_now_add=True)

    result_data = models.BinaryField(null=True)
    
    def set_results(self, data):
        json_data = json.dumps(data)  
        compressed_data = zlib.compress(json_data.encode('utf-8')) 
        self.result_data = compressed_data

    def get_results(self):
        decompressed_data = zlib.decompress(self.result_data)
        return json.loads(decompressed_data.decode('utf-8')) 
    