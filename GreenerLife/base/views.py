from django.db.models import Q
from django.shortcuts import render
from django.http import HttpResponse
from .models import EWasteSite, Clothing


def home(request):
    return render(request, 'base/home.html')

def e_waste(request):
    site = str(request.GET.get('ESite'))
    print(site)
    ewastes = EWasteSite.objects.filter(Q(site = site))
    context = {'ewastes': ewastes}

    return render(request, 'base/e_waste.html', context)

def clothing(request):
    site = str(request.GET.get('CSite'))
    print(site)
    clothings = Clothing.objects.filter(Q(district = site))
    context = {'clothings': clothings}

    return render(request, 'base/clothing.html', context)

