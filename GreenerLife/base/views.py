from django.db.models import Q
from django.shortcuts import render
from django.http import HttpResponse
from .models import EWasteSite, Clothing
from django.core import serializers



def home(request):
    return render(request, 'base/home.html')

def index(request):
    return render(request, 'base/index.html')

def about_us(request):
    return render(request, 'base/team.html')

def e_waste_classification(request):
    return render(request, 'base/e-waste-classification.html')

def e_waste(request):
    site = str(request.GET.get('ESite'))
    print(site)
    ewastes = EWasteSite.objects.all()#filter(Q(site = site))
    context = {'ewastes': ewastes}

    return render(request, 'base/e_waste.html', context)

def clothing(request):
    site = str(request.GET.get('CSite'))
    print(site)
    clothings = Clothing.objects.all()#filter(Q(district = site))
    context = {'clothings': clothings}

    return render(request, 'base/clothing.html', context)

