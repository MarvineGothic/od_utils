import cv2
import queue
import threading

import time
import collections


class BaseCamera:
    stream = None
    resolution = None
    width = None
    height = None

    def __init__(self, width=None, height=None):
        self.stream = cv2.VideoCapture(0)
        self.width = width
        self.height = height
        self.frame = None

        frame_width = int(self.stream.get(cv2.CAP_PROP_FRAME_WIDTH))
        frame_height = int(self.stream.get(cv2.CAP_PROP_FRAME_HEIGHT))

        if width and height:
            self.stream.set(3, self.width)
            self.stream.set(4, self.height)

        self.resolution = (frame_height, frame_width)
        self.q = queue.Queue()

    def add_overlay(self, buffer, format, layer, size):
        pass

    def remove_overlay(self, overlay):
        pass

    def read(self):
        success, self.frame = self.stream.read()
        if not success:
            return False, None

        def frame_render(queue_from_cam, frame):
            queue_from_cam.put(frame)

        cam = threading.Thread(target=frame_render, args=(self.q, self.frame))
        cam.start()
        cam.join()
        self.frame = self.q.get()
        self.q.task_done()
        return success, self.frame

    def show(self, window_name, frame):
        cv2.imshow(window_name, frame)
        if cv2.waitKey(1) == ord('q'):
            return False
        return True

    def isOpened(self):
        return self.stream.isOpened()

    def release(self):
        self.stream.release()
        cv2.destroyAllWindows()

    def start(self):
        pass

    def stop(self):
        self.release()


class FPS:
    def __init__(self, avarageof=50):
        self.frametimestamps = collections.deque(maxlen=avarageof)

    def __call__(self):
        self.frametimestamps.append(time.time())
        if (len(self.frametimestamps) > 1):
            return len(self.frametimestamps) / (self.frametimestamps[-1] - self.frametimestamps[0])
        else:
            return 0.0
