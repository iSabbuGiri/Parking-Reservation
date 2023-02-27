from rest_framework.serializers import ModelSerializer
from ..models import *

class CustomerSerializer(ModelSerializer):
    class Meta:
        model = Customer
        fields = '__all__'


class BookingSerializer(ModelSerializer):
    class Meta:
        model = Booking
        fields = '__all__'