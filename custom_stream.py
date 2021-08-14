import cv2
from imutils.video import FileVideoStream

from basecamera import BaseCamera


class CustomStream:
    def __init__(self, src=0, use_cv2=False):
        if use_cv2:
            self.obj = cv2.VideoCapture(int(src))
            self.stream = self.obj
        elif src == 0:
            self.obj = BaseCamera(src)
            self.stream = self.obj.stream
        elif src != 0:
            self.obj = FileVideoStream(src)
            self.stream = self.obj.stream

    def show(self, window_name, frame):
        cv2.imshow(window_name, frame)
        if cv2.waitKey(1) == ord('q'):
            return False
        return True

    def isOpened(self):
        return self.stream.isOpened()

    def start(self):
        if isinstance(self.obj, cv2.VideoCapture):
            return self
        self.obj.start()
        return self

    def read(self):
        if isinstance(self.obj, cv2.VideoCapture) or isinstance(self.obj, BaseCamera):
            return self.obj.read()
        return not self.obj.stopped, self.obj.read()

    def stop(self):
        if isinstance(self.obj, cv2.VideoCapture):
            self.obj.release()
        else:
            self.obj.stop()

    def set(self, propId, value):
        self.stream.set(propId, value)

    def get(self, propId):
        return self.stream.get(propId)

    @staticmethod
    def setHudText(frame, text, org):
        cv2.putText(frame, text, org, cv2.FONT_HERSHEY_SIMPLEX, 0.6, (0, 0, 255), thickness=2)

    @staticmethod
    def resizeFrame(frame, scale):
        width = int(frame.shape[1] * scale / 100)
        height = int(frame.shape[0] * scale / 100)
        dim = (width, height)
        return cv2.resize(frame, dim, interpolation=cv2.INTER_AREA)
