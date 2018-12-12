from grovepi import *

import numpy
import requests

class CameraTriggerButton(object):

    def __init__(
            self,
            imageCaptureEndpoint = "",
            sendToHubCallback = None):
        self.imageCaptureEndpoint = imageCaptureEndpoint
        self.sendToHubCallback = sendToHubCallback
        # Connect the Grove Button to digital port D3
        # SIG,NC,VCC,GND
        button = 5
        pinMode(button,"INPUT")

    def __invoke_camera_module(self):
        headers = {'Content-Type': 'application/json'}
        response = requests.get(self.imageCaptureEndpoint)
        try:
            print("Response from image capture service: (" + str(response.status_code) + ") ")
        except Exception:
            print("Response from image capture service (status code): " + str(response.status_code))

    def start(self):
        while True:
            if digitalRead(button) == 1:
                self.__invoke_camera_module()
                self.sendToHubCallback("ButtonClicked")