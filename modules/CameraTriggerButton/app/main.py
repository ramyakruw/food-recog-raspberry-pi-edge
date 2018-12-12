import os
import random
import sys
import time

import iothub_client
# pylint: disable=E0611
# Disabling linting that is not supported by Pylint for C extensions such as iothub_client. See issue https://github.com/PyCQA/pylint/issues/1955 
from iothub_client import (IoTHubModuleClient, IoTHubClientError, IoTHubError,
                           IoTHubMessage, IoTHubMessageDispositionResult,
                           IoTHubTransportProvider)

import button
from button import CameraTriggerButton

# global counters
SEND_CALLBACKS = 0

def send_to_Hub_callback(strMessage):
    message = IoTHubMessage(bytearray(strMessage, 'utf8'))
    hubManager.send_event_to_output("bottonout", message, 0)

# Callback received when the message that we're forwarding is processed.
def send_confirmation_callback(message, result, user_context):
    global SEND_CALLBACKS
    SEND_CALLBACKS += 1

class HubManager(object):

    def __init__(
            self,
            messageTimeout,
            protocol,
            verbose):
        '''
        Communicate with the Edge Hub

        :param int messageTimeout: the maximum time in milliseconds until a message times out. The timeout period starts at IoTHubClient.send_event_async. By default, messages do not expire.
        :param IoTHubTransportProvider protocol: Choose HTTP, AMQP or MQTT as transport protocol.  Currently only MQTT is supported.
        :param bool verbose: set to true to get detailed logs on messages
        '''
        self.messageTimeout = messageTimeout
        self.client_protocol = protocol
        self.client = IoTHubModuleClient()
        self.client.create_from_environment(protocol)
        self.client.set_option("messageTimeout", self.messageTimeout)
        self.client.set_option("product_info","edge-camera-trigger-button")
        if verbose:
            self.client.set_option("logtrace", 1)#enables MQTT logging

    def send_event_to_output(self, outputQueueName, event, send_context):
        self.client.send_event_async(outputQueueName, event, send_confirmation_callback, send_context)


def main(imageCaptureEndpoint = ""):
    try:
        print ( "Camera trigger button Edge Module. Press Ctrl-C to exit." )
        try:
            global hubManager
            hubManager = HubManager(10000, IoTHubTransportProvider.MQTT, verbose)
        except IoTHubError as iothub_error:
            print ( "Unexpected error %s from IoTHub" % iothub_error )
            return
        with CameraTriggerButton(imageCaptureEndpoint, send_to_Hub_callback) as cameraTriggerButton:
            cameraTriggerButton.start()
    except KeyboardInterrupt:
        print ( "Camera trigger button module stopped" )

if __name__ == '__main__':
    try:
        IMAGE_CAPTURE_ENDPOINT = os.getenv('IMAGE_CAPTURE_ENDPOINT', "")

    except ValueError as error:
        print ( error )
        sys.exit(1)

    main(IMAGE_CAPTURE_ENDPOINT)

