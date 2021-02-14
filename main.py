from gpiozero import MotionSensor
import os
import time
import datetime
import messenger
import camwrapper

# GPIO-4 (Pin 7) - PIR sensor.
pir = MotionSensor(4)


# create directories and configuration files.
def initialize():
    directory = "video/"
    if not os.path.isdir(directory):
        os.makedirs(directory)


# get filename based on current date time.
def get_file_name():
    return datetime.datetime.now().strftime("video/%Y-%m-%d_%H.%M.%S.h264")


# ensure there is no more than 6 latest files stored.
def clean_storage():
    recordings = os.listdir("video/")
    if len(recordings) > 5:
        try:
            os.remove("video/" + recordings[len(recordings) - 1])
        except Exception as e:
            print(f"Failed to delete {recordings[len(recordings) - 1]}. Reason: {e}")


# write event into log file
def log_event(event):
    print(event)
    with open('activity.log', 'a', encoding='utf-8') as f:
        f.write(event + '\n')


# main program function
def main():
    initialize()
    print("Monitoring for activity...")
    while True:
        filename = get_file_name()
        pir.wait_for_motion()
        event = f'{datetime.datetime.now().strftime("%Y-%m-%d_%H.%M.%S")} Movement detected.'
        log_event(event)
        # email = messenger.Email('marcin.karpik@gmail.com', 'Alert: movement detected', 'Movement detected:\n')
        # email.send_email()
        cam = camwrapper.CameraWrapper()
        cam.video_capture(filename=filename, length=30)
        clean_storage()
        time.sleep(2)


if __name__ == "__main__":
    main()
