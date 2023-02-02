from rest_framework.views import APIView
from rest_framework.response import Response
from ..models import *
from .serializers import *


class CustomerListApi(APIView):

    
    def get(self,request):
        customer_objs = Customer.objects.all()
        serializer = CustomerSerializer(customer_objs, many=True)
        return Response({'status': 200, 'payload' : serializer.data})

    def post(self,request):
        serializer = CustomerSerializer(data=request.data)
        if serializer.is_valid():
            serializer.save()
            return Response({'status' : 200, 'payload': serializer.data, 'message':'your data is created'})

        return Response({'status': 403, 'payload': serializer.data, 'message': 'something went wrong'})  

class CustomerDetailApi(APIView):

    def get(self,request,pk):
        try:
            customer_obj = Customer.objects.get(pk=pk)
            serializer = CustomerSerializer(customer_obj)
            return Response({'status': 200, 'payload' : serializer.data})
        except Customer.DoesNotExist:
            return Response({'status': 404, 'message' : 'Customer not found'})    


    def put(self,request):
        try:
            id = request.GET.get('id')
            customer_obj = Customer.objects.get(id = id)
            serializer = CustomerSerializer(customer_obj, data=request.data, partial=False)
            if not serializer.is_valid():
                print(serializer.errors)
                return Response({'status':403, 'errors':serializer.errors, 'message': 'something went wrong'})

            serializer.save()    
            return Response({'status':200, 'payload': serializer.data, 'message': 'your data is created'})

        except Exception as e:
            print(e)
            return Response({'status': 403, 'message': 'Invalid id'})    

    def delete(self,request):
        try:
            id = request.GET.get('id')
            customer_objs = Customer.objects.get(id = id)
            customer_objs.delete()
            return Response({'status':200, 'message': 'deleted'})
        except Exception as e:
            print(e)
            return Response({'status':403, 'message': 'Invalid id'})    

