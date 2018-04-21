from django.shortcuts import render, get_object_or_404
from django.http import JsonResponse
from django.views.decorators.csrf import csrf_exempt

import boto3

from .forms import LocationForm, PhoneForm
from .models import Location


@csrf_exempt
def poll_location(request, unique_link):
    location = Location.objects.get(unique_link=unique_link)
    if location:
        return JsonResponse({'longitude': location.longitude,
                             'latitude': location.latitude})


def show_location(request, unique_link):
    location = get_object_or_404(Location, unique_link=unique_link)
    return render(request, 'location/show_location.html', {'location': location})


def get_location(request, unique_link):
    if request.method == 'POST':
        form = PhoneForm(request.POST)
        if form.is_valid():
            new_request = form.save(commit=False)
            new_request.request_location()
            new_request.save()
            return render(request, 'location/show_location.html', {'location': new_request,
                                                                   'note': 'Emergency Services Now Have Your Location'})
    form = PhoneForm()
    return render(request, 'location/get_location.html', {'form': form})


def request_location(request):
    if request.method == 'POST':
        form = PhoneForm(request.POST)
        if form.is_valid():
            new_request = form.save(commit=False)
            new_request.request_location()
            new_request.save()
    form = PhoneForm()
    return render(request, 'location/request_location.html', {'form': form})
