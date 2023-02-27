from django.urls import path
from .views import CustomerView, BookingView
from rest_framework import routers



router = routers.DefaultRouter()
router.register('customer', CustomerView)
router.register('booking', BookingView)

urlpatterns = [
#     path('customers/', CustomerList.as_view(),name='ap1-v1-parking-view'),
#     path('customer/<int:pk>/', CustomerDetailApi.as_view(),name='ap1-v2-parking-view')

]

urlpatterns += router.urls
