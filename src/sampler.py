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

externalVMManager.launchVM()
def sample(samplePath):
    externalVMManager.executeFile(samplePath)
    loggingUtil.sync_packet_capture_for(60)
    loggingUtil.export_packet_log(True)
    externalVMManager.cycleVM()

def passive():
    loggingUtil.sync_packet_capture_for(60)
    externalVMManager.cycleVM()

def enableLogging():
    print("Logging Enabled")

def disableLogging():
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
    parsedSignal = stringData[0:7]
    print("Parsed signal: %s" % (parsedSignal))
    if parsedSignal == SAMPLE_SIGNAL:
        parsedData = stringData[8:len(stringData)]
        print("Received Path: %s" % (parsedData))
        sample(stringData[8:len(stringData)])
        print("Sending ready message")
        clientsocket.sendall("Ready")
    if parsedSignal == PASSIVE_SIGNAL:
        # Do not execute a sample
        print("Passive Signal")
        passive()
        print("Sending ready message")
        clientsocket.sendall("Ready")
