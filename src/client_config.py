# TODO: Make these settings transmitted to the test machines, instead of relying on local storage.

import os

# IP of the Server samplermanager.py
SERVER_IP = "127.0.0.1"
# SERVER_IP = '10.0.0.8'
# Port of the Server samplermanager.py
SERVER_PORT = 5000
# Buffer size for the socket
BUFFER_SIZE = 2000
# String fragment to indicate sampling on client sampler.py
SAMPLE_SIGNAL = 'Sample'
# String fragment to indicate passiveness on client sampler.py
PASSIVE_SIGNAL = 'Passive'
# String fragment to indicate VM cycle
CYCLE_STRING = 'Cycle:'

# Name of the VM
VM_NAME = 'Windows'
# Windows username for the VM
VM_USERNAME = "M"
# Windows password for the VM
VM_PASSWORD = "computer"
# Name of the VM snapshot to restore after infection
VM_SNAPSHOT = "Before Infection"

EXPORT_DIR = os.path.abspath("/root/Desktop")
INTERFACE = 'eth0'
