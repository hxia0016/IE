from django.conf import settings
from django.core.files.base import ContentFile
from django.core.files.storage import default_storage
from django.db.models import Q
from django.shortcuts import render
from django.http import HttpResponse
from .models import EWasteSite, Clothing
from django.core import serializers
import base64
import os
import cv2
from .model.garbageDetection import modelThread


model = modelThread()
model.__int__("./base/model/")
model.model.summary
img = cv2.imread(".\static\images\coffee.png")
model.predict(img)


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
    ewastes = EWasteSite.objects.all()
    context = {'ewastes': ewastes}

    return render(request, 'base/e_waste.html', context)

def clothing(request):
    site = str(request.GET.get('CSite')) if request.GET.get('CSite') != None else ''
    print(site)
    clothings = Clothing.objects.all()
    context = {'clothings': clothings}

    return render(request, 'base/clothing.html', context)


def garbage(request):
    return render(request, 'base/garbage.html', )

def getbase64byndarray(pic_img):
    retval, buffer = cv2.imencode('.jpg', pic_img)
    pic_str = base64.b64encode(buffer)
    return pic_str.decode()


def garbageClassification(request):
    print("in")
    try:
        # 当不使用JS时
        # image = request.FILES.get('garbageImage')
        # 当使用ajax时
        # 得到img文件
        image = request.FILES['garbageImage']
        print(image)
        path = default_storage.save('' + image.name, ContentFile(image.read()))
        print(path.__str__())
        # 保存图像
        path = os.path.join(settings.MEDIA_ROOT, path)
        img = cv2.imread(path)

        img = cv2.resize(img, (224, 224))
        res,idx = model.predict(img)
        res = base64.b64encode(res)
        print("predict classes index",idx)
        return HttpResponse(res)
    except:
        return HttpResponse("<p>图片上传不成功</p>")