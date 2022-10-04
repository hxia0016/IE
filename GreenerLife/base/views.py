from django.conf import settings
from django.core.files.base import ContentFile
from django.core.files.storage import default_storage
from django.db.models import Q
from django.shortcuts import render
from django.http import StreamingHttpResponse
from django.http import HttpResponse

from .camera import camDetect
from .models import EWasteSite, Clothing
from django.core import serializers
import base64
import os
import cv2
from .model.garbageDetection import GarbageModel
from .model.educationGame import EudcationGame
import tensorflow
import numpy as np
import pathlib


path = pathlib.Path.cwd()
path = path / 'base' / 'model'
tensorflow.keras.backend.clear_session()
os.environ['TF_CPP_MIN_LOG_LEVEL'] = '3'
os.environ["CUDA_VISIBLE_DEVICES"] = "-1"
# model = GarbageModel("./GreenerLife/base/model/")
model = GarbageModel(path)
# model = ModelThread("./base/model/")
# img = cv2.imread("./GreenerLife/static / images / coffee.png")
img = cv2.imread("./static / images / coffee.png")
# model.predict(img)
# edu_game = EudcationGame("./GreenerLife/base/model/")
edu_game = EudcationGame(path)


def index(request):
    return render(request, 'base/index.html')


def about_us(request):
    return render(request, 'base/team.html')


def e_waste_classification(request):
    site = str(request.GET.get('ESite')) if request.GET.get('ESite') != None else ''
    print(site)
    ewastes = EWasteSite.objects.all()
    context = {'ewastes': ewastes}
    return render(request, 'base/e-waste.html', context)


def e_waste(request):
    site = str(request.GET.get('ESite')) if request.GET.get('ESite') != None else ''
    print(site)
    ewastes = EWasteSite.objects.all()
    context = {'ewastes': ewastes}

    return render(request, 'base/e-waste-classification.html', context)


def clothing(request):
    site = str(request.GET.get('CSite')) if request.GET.get('CSite') != None else ''
    print(site)
    clothings = Clothing.objects.all()
    context = {'clothings': clothings}

    return render(request, 'base/clothing.html', context)


def garbage(request):
    return render(request, 'base/garbage.html', )


def garbage_video(request):
    return render(request, 'base/garbage-webcam.html', )


def garbageClassification(request):
    image = request.POST['data']
    head, image = image.split(',')
    imagedata = base64.b64decode(image)
    nparr = np.frombuffer(imagedata, np.uint8)
    img = cv2.imdecode(nparr, cv2.IMREAD_COLOR)
    img, b = model.predict(img)
    ret, jpeg = cv2.imencode(".jpg", img)
    image = head + ',' + str(base64.b64encode(jpeg))[2:-1]
    return HttpResponse(image, content_type='multipart/x-mixed-replace; boundary=frame')


def gen_garbage(camera):
    while True:
        frame = camera.get_frame_garbage(model)
        yield (b'--frame\r\n'
               b'Content-Type: image/jpeg\r\n\r\n' + frame + b'\r\n\r\n')


def gen_game(camera):
    while True:
        frame = camera.get_frame_game(edu_game)
        yield (b'--frame\r\n'
               b'Content-Type: image/jpeg\r\n\r\n' + frame + b'\r\n\r\n')


def video(request):
    garbage_cam = camDetect(model)
    return HttpResponse(gen_garbage(garbage_cam), content_type='multipart/x-mixed-replace; boundary=frame')


def edu(request):
    edu_game.flag = False
    edu_game.updateLocation()
    return render(request, 'base/edu.html')


def edu_video(request):
    image = request.POST['data']
    head, image = image.split(',')
    imagedata = base64.b64decode(image)
    nparr = np.frombuffer(imagedata, np.uint8)
    image = cv2.imdecode(nparr, cv2.IMREAD_COLOR)
    img = edu_game.run(image)
    # ret, jpeg = cv2.imencode(".jpg", img)
    # image = head + ',' + str(base64.b64encode(jpeg))[2:-1]
    if not edu_game.flag:
        ret, jpeg = cv2.imencode(".jpg", img)
        img = head + ',' + str(base64.b64encode(jpeg))[2:-1]
    else:
        frame = cv2.flip(image, 1)
        img = cv2.putText(frame, "You Lost!", (250, 240), cv2.FONT_HERSHEY_PLAIN, 3,
                          (0, 0, 255), 3)
        img = cv2.putText(img, "score : " + str(edu_game.score), (250, 340), cv2.FONT_HERSHEY_PLAIN, 3,
                          (0, 0, 255), 3)
        ret, jpeg = cv2.imencode(".jpg", img)
        img = head + ',' + str(base64.b64encode(jpeg))[2:-1]
    return HttpResponse(img, content_type='multipart/x-mixed-replace; boundary=frame')
