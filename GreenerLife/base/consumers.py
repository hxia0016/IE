import datetime
import json
import base64
import os
import pathlib

import cv2
import numpy as np
import requests
import tensorflow
from asgiref.sync import async_to_sync
from channels.generic.websocket import  WebsocketConsumer

from IE.GreenerLife.base.model.educationGame import EudcationGame
from IE.GreenerLife.base.model.garbageDetection import GarbageModel

path = pathlib.Path.cwd()

print(path)
tensorflow.keras.backend.clear_session()
# os.environ['TF_CPP_MIN_LOG_LEVEL'] = '3'
os.environ["CUDA_VISIBLE_DEVICES"] = "-1"
model = GarbageModel(path / 'base' / 'model')
img = cv2.imread(str(path / 'base' / 'model' / 'bin.png'))
model.predict(img)
edu_game = EudcationGame(path/ 'base' / 'model')


class VideoConsumer(WebsocketConsumer):
    # websocket建立连接时执行方法
    def connect(self):
        # 从url里获取聊天室名字，为每个房间建立一个频道组
        self.room_name = self.scope['url_route']['kwargs']['room_name']
        self.room_group_name = 'chat_%s' % self.room_name
        edu_game.flag = False
        edu_game.reset_game()

        # 将当前频道加入频道组
        async_to_sync(self.channel_layer.group_add)(
            self.room_group_name,
            self.channel_name
        )

        # 接受所有websocket请求
        self.accept()

    # websocket断开时执行方法
    def disconnect(self, close_code):
        async_to_sync(self.channel_layer.group_discard)(
            self.room_group_name,
            self.channel_name
        )

        # 从websocket接收到消息时执行函数

    def receive(self, text_data):
        text_data_json = json.loads(text_data)
        message = text_data_json['message']
        head, image = message.split(',')
        imagedata = base64.b64decode(image)
        nparr = np.frombuffer(imagedata, np.uint8)
        img = cv2.imdecode(nparr, cv2.IMREAD_COLOR)
        back_data = "#"
        if self.room_name == "garbage":
            img, b = model.predict(img)
            ret, jpeg = cv2.imencode(".jpg", img)
            back_data = head + ',' + str(base64.b64encode(jpeg))[2:-1]
        elif self.room_name == "game":

            if not edu_game.flag:
                img = edu_game.run(img)
                ret, jpeg = cv2.imencode(".jpg", img)
                back_data = head + ',' + str(base64.b64encode(jpeg))[2:-1]
            else:
                frame = cv2.flip(img, 1)
                img = cv2.putText(frame, "You Lost!", (250, 240), cv2.FONT_HERSHEY_PLAIN, 3,
                                  (0, 0, 255), 3)
                img = cv2.putText(img, "score : " + str(edu_game.score), (250, 340), cv2.FONT_HERSHEY_PLAIN, 3,
                                  (0, 0, 255), 3)
                ret, jpeg = cv2.imencode(".jpg", img)
                back_data = head + ',' + str(base64.b64encode(jpeg))[2:-1]
        self.send(text_data=json.dumps({
            'message': back_data
        }))

    # 从频道组接收到消息后执行方法
    def chat_message(self, event):
        message = event['message']
        datetime_str = datetime.datetime.now().strftime('%Y-%m-%d %H:%M:%S')

        # 通过websocket发送消息到客户端
        self.send(text_data=json.dumps({
            'message': f'{datetime_str}:{message}'
        }))
