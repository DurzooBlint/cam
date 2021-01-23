from gpiozero import MotionSensor
from picamera import PiCamera
import os
import time
import datetime

# GPIO-4 (Pin 7) - PIR sensor
pir = MotionSensor(4)
camera = PiCamera()


def get_file_name():
    return datetime.datetime.now().strftime("video/%Y-%m-%d_%H.%M.%S.h264")


def clean_storage():
    recordings = os.listdir("video/")
    if len(recordings) > 5:
        try:
            os.remove(recordings(len(recordings) - 1))
        except Exception as e:
            print(f"Failed to delete {recordings(len(recordings) - 1)}. Reason: {e}")


def main():
    while True:
        filename = get_file_name()
        pir.wait_for_motion()
        print(f'{datetime.datetime.now().strftime("%Y-%m-%d_%H.%M.%S")} Movement detected.')
        camera.start_recording(filename)
        # Record for 20 seconds
        camera.wait_recording(20)
        camera.stop_recording()
        clean_storage()
        time.sleep(2)


if __name__ == "__main__":
    main()
