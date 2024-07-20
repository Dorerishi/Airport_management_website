from django.urls import path
from . import views

urlpatterns = [
    path('',views.base,name='base'),
    path('schedule/', views.schedule, name='schedule'),
    path('add-arrival/', views.add_arrival, name='add_arrival'),
    path('arrival-success/', views.arrival_success, name='arrival_success'),
    path('add-passenger/',views.add_passenger, name='add_passenger'),
    path('passenger-success/', views.passenger_success, name='passenger_success'),
    path('fl_no/', views.cust, name='fl_no'),
    path('update-passenger/',views.update_passenger,name='update_passenger'),
    path('delete-passenger/',views.del_passenger,name='delete_passenger'),
    path('delete-passenger-success/',views.delete_passenger_success,name='delete_passenger_success'),
    path('update-arrival/', views.update_arrival_view, name='update_arrival'),
    path('update-success/', views.update_success, name='update_success'),
    path('del_ar_del/', views.delete_record_view, name='delete'),
    path('deletion_success/',views.delete_success,name="delete_success"),
]