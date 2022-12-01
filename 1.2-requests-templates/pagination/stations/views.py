from django.core.paginator import Paginator
from django.shortcuts import render, redirect
from django.urls import reverse

import csv
from django.conf import settings

STATIONS_LIST = []

with open(settings.BUS_STATION_CSV, newline='') as csvfile:
    listing = csv.DictReader(csvfile)
    for row in listing:
        STATIONS_LIST.append((row['Name'], row['Street'], row['District']))

def index(request):
    return redirect(reverse('bus_stations'))


def bus_stations(request):
    # получите текущую страницу и передайте ее в контекст
    # также передайте в контекст список станций на странице
#    context = {
    #     'bus_stations': ...,
    #     'page': ...,
#    }
    page_number = int(request.GET.get("page", 1))
    paginator = Paginator(STATIONS_LIST, 10)
    bus_stations = paginator.get_page(page_number)
    page = paginator.get_page(page_number)
    context = {
        'bus_stations': bus_stations,
        'page': page,
    }
    return render(request, 'stations/index.html', context)
