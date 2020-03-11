# This Python script runs on the host OS of the machine that will control the VM enviroments.
# It acts as a client that receives signals from the samplermanager. 

import socket, time, threading
import external_VM_Manager as externalVMManager
# import client.external_VM_Manager as externalVMManager
import logging_util as loggingUtil
import client_config as clientconfig

IP = clientconfig.SERVER_IP
PORT = clientconfig.SERVER_PORT
BUFFER_SIZE = clientconfig.BUFFER_SIZE
SAMPLE_SIGNAL = clientconfig.SAMPLE_SIGNAL
PASSIVE_SIGNAL = clientconfig.PASSIVE_SIGNAL

samplingComplete = False

externalVMManager.launch_vm()


def sample(sample_path, incubation_time):
    externalVMManager.execute_file_in_vm(sample_path)
    loggingUtil.sync_packet_capture_for(incubation_time)
    loggingUtil.export_packet_log(False)
    externalVMManager.cycle_vm()


def passive():
    # loggingUtil.sync_packet_capture_for(60)
    # externalVMManager.cycleVM()
    print("Not implemented")


def enable_logging():
    print("Logging Enabled")


def disable_logging():
    print("Logging Disabled")


# Connect to the SamplerManager server
clientsocket = socket.socket(socket.AF_INET, socket.SOCK_STREAM)
clientsocket.connect((IP, PORT))

# Probably change this to while VM ready to sample or something
# Wait for a signal from the SamplerManager server and parsed
# this signal into something meaningful
while True:
    data = clientsocket.recv(BUFFER_SIZE)
    stringData = data.decode()
    parsedSignal = stringData[0:6]
    print("Parsed signal: %s" % parsedSignal)
    if parsedSignal == SAMPLE_SIGNAL:
        print("Sample Signal Received")
        # TODO: Make this work when incubation_time is greater than 2 digits
        parsed_incubation_time = stringData[6:8]
        parsed_path = stringData[10:len(stringData)]
        print("Received incubation time: %s" % parsed_incubation_time)
        print("Received path: %s" % parsed_path)
        sample(parsed_path, parsed_incubation_time)
        print("Sending ready message")
        clientsocket.sendall("Ready")
    elif parsedSignal == PASSIVE_SIGNAL:
        # Do not execute a sample
        print("Passive Signal")
        passive()
        print("Sending ready message")
        clientsocket.sendall("Ready")
