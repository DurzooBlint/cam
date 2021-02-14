from picamera import PiCamera
import time


class CameraWrapper():
    def __init__(self):
        self.camera = PiCamera()

    def image_capture(self, filename, thumbnail=False):
        self.camera.start_preview()
        # Camera warm-up time
        time.sleep(2)
        if thumbnail:
            self.camera.capture(filename, resize=(320, 240))
        else:
            self.camera.capture(filename)

    def video_capture(self, filename, length=30):
        self.camera.start_recording(filename)
        self.camera.wait_recording(length)
        self.camera.stop_recording()
