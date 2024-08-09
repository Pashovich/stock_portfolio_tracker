from django.db import models
from django.conf import settings


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

    def __str__(self):
        return self.name
    
    def delete(self, *args, **kwargs):
    
        self.shares.all().delete()
        super().delete(*args, **kwargs)