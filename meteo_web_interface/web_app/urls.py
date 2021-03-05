from django.urls import path
from . import views


#path('url', '<view name>', name=<''url name>)
urlpatterns = [
    path('', views.temperature_view, name='temperature_view_main'),
    path('temperature', views.temperature_view, name='temperature_view'),
    path('pressure', views.pressure_view, name='pressure_view'),
    path('light', views.light_view, name='light_view'),
]
