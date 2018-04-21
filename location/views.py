from datetime import datetime

from django.shortcuts import render, get_object_or_404, redirect
from django.http import JsonResponse
from django.views.decorators.csrf import csrf_exempt

import boto3

from .forms import LocationForm, PhoneForm
from .models import Location


@csrf_exempt
def poll_location(request, unique_link):
    try:
        location = Location.objects.get(unique_link=unique_link)
        if location.found:
            return JsonResponse({'status': 'found',
                                 'longitude': location.longitude,
                                 'latitude': location.latitude})
        else:
            return JsonResponse({'status': 'not_found'})
    except Location.DoesNotExist:
        return JsonResponse({'status': 'not_found'})


def show_location(request, unique_link):
    location = get_object_or_404(Location, unique_link=unique_link)
    return render(request, 'location/show_location.html', {'location': location})


@csrf_exempt
def get_location(request, unique_link):
    if request.method == 'POST':
        form = LocationForm(request.POST)
        if form.is_valid():
            cd = form.cleaned_data
            try:
                location = Location.objects.get(unique_link=unique_link)
                location.longitude = cd['longitude']
                location.latitude = cd['latitude']
                location.found = datetime.now()
                location.save()
                return render(request, 'location/thanks_location.html', {'location': location,
                                                                       'note': 'Emergency Services Now Have Your Location'})
            except Location.DoesNotExist:
                # Demos always fail!
                location = Location.objects.get(id=1)
                return render(request, 'location/thanks_location.html', {'location': location,
                                                                       'note': 'Emergency Services Now Have Your Location'})
    form = LocationForm()
    return render(request, 'location/get_location.html', {'form': form})


def request_location(request):
    if request.method == 'POST':
        form = PhoneForm(request.POST)
        if form.is_valid():
            cd = form.cleaned_data
            new_location = Location.create(phone=cd['number'])
            new_location.request_location(request.build_absolute_uri())
            return redirect('location:show', unique_link=new_location.unique_link)
    form = PhoneForm()
    return render(request, 'location/request_location.html', {'form': form})
