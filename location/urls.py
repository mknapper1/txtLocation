from django.urls import path

from . import views

urlpatterns = [
    path('poll/<uuid:unique_link>/', views.poll_location),
    path('get/<uuid:unique_link>/', views.get_location),
    path('request/', views.request_location),
    path('show/<uuid:unique_link>/', views.show_location),
]
