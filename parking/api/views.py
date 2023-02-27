from datetime import datetime, timedelta
from rest_framework.views import APIView
from rest_framework.viewsets import ModelViewSet
from rest_framework.response import Response
from ..models import Customer, Booking
from .serializers import CustomerSerializer, BookingSerializer
from rest_framework import status
from django.http import Http404
from rest_framework import generics
from rest_framework.pagination import PageNumberPagination
from django_filters.rest_framework import DjangoFilterBackend


# class CustomerListApi(APIView):
#     def get(self,request):
#         customer_objs = Customer.objects.all()
#         serializer = CustomerSerializer(customer_objs, many=True)
#         return Response(serializer.data, status=status.HTTP_200_OK)

#     def post(self,request):
#         serializer = CustomerSerializer(data=request.data)
#         if serializer.is_valid():
#             serializer.save()
#             return Response(serializer.data, status=status.HTTP_201_CREATED)
#         return Response(serializer.data, status=status.HTTP_400_BAD_REQUEST)  

# class CustomerDetailApi(APIView):
#     def get(self,request, *args, **kwargs):
#         try:
#             customer_obj = Customer.objects.get(pk=kwargs['pk'])
#         except Customer.DoesNotExist:
#            raise Http404
#         else:
#             serializer = CustomerSerializer(customer_obj)
#             return Response(serializer.data, status=status.HTTP_200_OK)    
    
#     def put(self,request,pk):
#         try:
#             customer_obj = Customer.objects.get(pk=pk)
#         except Customer.DoesNotExist:
#             raise Http404

#         else:  
#             serializer = CustomerSerializer(customer_obj, request.data)
#             if serializer.is_valid():
#                 serializer.save()
#                 return Response(serializer.data,status=status.HTTP_200_OK)  
#             else:
#                 return Response(serializer.errors,status=status.HTTP_400_BAD_REQUEST)    
       
            
#     def delete(self,request,pk):
#         try:
#             customer_objs = Customer.objects.get(pk=pk)
#         except Customer.DoesNotExist:
#             raise Http404
#         else:    
#             customer_objs.delete()
#             return Response(status=status.HTTP_200_OK)

class StandardPagination(PageNumberPagination):
    page_size = 1
    page_size_query_param = 'page_size'       

class CustomerView(ModelViewSet):
    queryset = Customer.objects.all()
    serializer_class = CustomerSerializer
    pagination_class = StandardPagination

    # def create(self, request):
    #     name = self.request.data.get('name')
    #     if name == 'Rajan':
    #         return Response({'message':"Rajan is not allowed"}, status=status.HTTP_400_BAD_REQUEST)
    #     return super().create(request)

# class CustomerDetail(generics.RetrieveUpdateDestroyAPIView):
#     queryset = Customer.objects.all()
#     serializer_class = CustomerSerializer
    
    # def update(self, request, *args, **kwargs):
#         instance = self.get_object()

#         if instance.license_plate != request.data['license_plate']:
#             return Response({'message':"License cannot be updated"}, status=status.HTTP_400_BAD_REQUEST)

#         return super().update(request, *args, **kwargs)    

#         # serializer = self.get_serializer(instance, data=request.data, partial=True)
#         # serializer.is_valid(raise_exception=True)
#         # self.perform_update(serializer)

#     def destroy(self, request, *args, **kwargs):
#         instance = self.get_object()
#         if instance.name == 'Rajan':
#             return Response({'message':"Rajan cannot be deleted"}, status=status.HTTP_400_BAD_REQUEST)
#         return super().destroy(request, *args, **kwargs)



class BookingView(ModelViewSet):
    queryset = Booking.objects.all()
    serializer_class = BookingSerializer
    pagination_class = StandardPagination
    filter_backend = [DjangoFilterBackend]
    filtersets_fields = ['customer', 'booking_date', 'parking_bay']

    def validate_booking(self, customer, booking_date, parking_bay, instance=None):

        booking_date = datetime.strptime(self.request.data.get('booking_date'), '%Y-%m-%d')

        # Check if booking is made atleast 24h in advance 
        if booking_date < datetime.now() + timedelta(days=1):
            return Response({'message':'Bookings must be made atleast 24 hours in adavnce'}, status=status.HTTP_400_BAD_REQUEST)

        # Check if free bay is available within a given date
        if instance:
            bay_booked = Booking.objects.exclude(pk=instance.pk).filter(booking_date=booking_date, parking_bay=parking_bay)
        else:
            bay_booked = Booking.objects.filter(booking_date=booking_date, parking_bay=parking_bay)
        if bay_booked.exists():
            return Response({'message':'parkingbay already booked for the given date'}, status=status.HTTP_400_BAD_REQUEST)

        # Check if customer has already booked for same day
        if instance:
            bay_booked_for_customer = Booking.objects.exclude(pk=instance.pk).filter(customer= customer, booking_date = booking_date)
        else:    
            bay_booked_for_customer = Booking.objects.filter(customer= customer, booking_date = booking_date)    
        if bay_booked_for_customer.exists():
            return Response({'message':'Customer has already booked for this date'}, status=status.HTTP_400_BAD_REQUEST)    
        
    def create(self, request, *args, **kwargs):
        customer = self.request.data.get('customer')
        booking_date = self.request.data.get('booking_date')
        parking_bay = self.request.data.get('parking_bay')

        result = self.validate_booking(customer, booking_date, parking_bay)

        if result:
            return result

        return super().create(request)   
    
    def list(self, request, *args, **kwargs):
        print(request.user) 

        return super().list(request) 
        
        
        
        # Check if booking is made atleast 24h in advance 
        # if booking_date < datetime.now() + timedelta(days=1):
        #     return Response({'message':'Bookings must be made atleast 24 hours in adavnce'}, status=status.HTTP_400_BAD_REQUEST)

        # # Check if free bay is available within a given date
        # bay_booked = Booking.objects.filter(booking_date=booking_date, parking_bay=parking_bay)
        # if bay_booked.exists():
        #     return Response({'message':'parkingbay already booked for the given date'}, status=status.HTTP_400_BAD_REQUEST)

        # # Check if customer has already booked for same day
        # bay_booked_for_customer = Booking.objects.filter(customer= customer, booking_date = booking_date)    
        # if bay_booked_for_customer.exists():
        #     return Response({'message':'Customer has already booked for this date'}, status=status.HTTP_400_BAD_REQUEST)

        # return super().create(request)    

    def update(self, request, *args, **kwargs):
        customer = self.request.data.get('customer')
        booking_date = self.request.data.get('booking_date')
        parking_bay = self.request.data.get('parking_bay')

        instance = self.get_object()

        result = self.validate_booking(customer, booking_date, parking_bay, instance)

        if result:
            return result
        
        return super().update(request, *args, **kwargs)  

        # Check if booking is made atleast 24h in advance 
        # if booking_date < datetime.now() + timedelta(days=1):
        #     return Response({'message':'Bookings must be made atleast 24 hours in adavnce'}, status=status.HTTP_400_BAD_REQUEST)

        # # Check if free bay is available within a given date
        # bay_booked = Booking.objects.exclude(pk=instance.pk).filter(booking_date=booking_date, parking_bay=parking_bay)
        # if bay_booked.exists():
        #     return Response({'message':'parkingbay already booked for the given date'}, status=status.HTTP_400_BAD_REQUEST)

        # # Check if customer has alr eady booked for same day
        # bay_booked_for_customer = Booking.objects.exclude(pk=instance.pk).filter(customer= customer, booking_date = booking_date)    
        # if bay_booked_for_customer.exists():
        #     return Response({'message':'Customer has already booked for this date'}, status=status.HTTP_400_BAD_REQUEST)

        # return super().update(request, *args, **kwargs)       

