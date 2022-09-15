from imutils.video import VideoStream
import cv2


class camDetect(object):
    def __init__(self, model):
        self.vs = VideoStream().start()
        self.model = model

    def __del__(self):
        self.vs.stop()

    def clean(self):
        cv2.destroyAllWindows()
    def start(self):
        self.vs = VideoStream().start()

    def predict_garbage(self, frame, model):
        res, idx = model.predict(frame)
        return (res, idx)

    def get_frame_garbage(self, model):
        frame = self.vs.read()
        (res, idx) = self.predict_garbage(frame, model)
        ret, jpeg = cv2.imencode('.jpg', res)
        return jpeg.tobytes()

    def get_frame_game(self, model):
        frame = self.vs.read()
        # frame = cv2.flip(frame, 1)
        res = self.game(frame, model)
        if not model.flag:
            ret, jpeg = cv2.imencode('.jpg', res)
        else:
            frame = cv2.flip(frame, 1)
            img = cv2.putText(frame, "You Lost!", (250, 240), cv2.FONT_HERSHEY_PLAIN, 3,
                              (0, 0, 255), 3)
            img = cv2.putText(img, "score : " + str(model.score), (250, 340), cv2.FONT_HERSHEY_PLAIN, 3,
                              (0, 0, 255), 3)

            ret, jpeg = cv2.imencode('.jpg', img)
            self.clean()
        return jpeg.tobytes()

    def game(self, frame, model):
        res = model.run(frame)
        return res
