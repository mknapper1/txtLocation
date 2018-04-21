from django.urls import path

from . import views

urlpatterns = [
    path('poll/<uuid:unique_link>/', views.poll_location, name='poll'),
    path('get/<uuid:unique_link>/', views.get_location, name='get'),
    path('request/', views.request_location, name='request'),
    path('show/<uuid:unique_link>/', views.show_location, name='show'),
]
