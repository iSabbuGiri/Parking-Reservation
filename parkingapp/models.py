from django.db import models

PARKING_BAY_CHOICES = (
    (1,1),
    (2,2),
    (3,3),
    (4,4)

)

class Customer(models.Model):
    name = models.CharField(max_length=200)
    license_plate = models.CharField(max_length=20, unique=True)

    class Meta:
        ordering= ['-id']

    def __str__(self):
        return self.name    


class Booking(models.Model):
    customer = models.ForeignKey(Customer, on_delete=models.CASCADE)
    parking_bay = models.PositiveIntegerField(choices=PARKING_BAY_CHOICES)
    booking_date = models.DateField()
    created_at = models.DateTimeField(auto_now_add=True)

    class Meta:
        ordering = ['-booking_date', 'created_at']

    def __str__(self):
        return self.name + ' ' + self.booking_date
