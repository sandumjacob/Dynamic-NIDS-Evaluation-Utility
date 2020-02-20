import subprocess, os, time
import client_config as client_config
# A library for integrating VBoxManage Bash scripting
# into Python 

VM_NAME = client_config.VM_NAME
VM_USERNAME = client_config.VM_USERNAME
VM_PASSWORD = client_config.VM_PASSWORD
VM_SNAPSHOT = client_config.VM_SNAPSHOT

VM_CMD_PATH = "c:\\windows\\system32\\cmd.exe"

def hookVM_CMD(filePath):
    command = "VBoxManage --nologo guestcontrol \"%s\" run --exe \"%s\" --username %s --password %s --wait-stdout" % (VM_NAME, VM_CMD_PATH, VM_USERNAME, VM_PASSWORD)

    print("Command to execute:\n", command)
    stream = os.popen(command, mode='w')
    print("Response: ", stream)
    # subprocess.run([command, "-1"])

def executeFile(filepath):
    command = "VBoxManage --nologo guestcontrol \"%s\" run --exe \"%s\" --username %s --password %s --wait-stdout" % (VM_NAME, filepath, VM_USERNAME, VM_PASSWORD)
    print("Command to execute:\n", command)
    stream = os.popen(command)
    print("Response: ", stream)

def listRunningVMs():
    command = "VBoxManage list runningvms" 
    print(os.system)

def launchVM():
    success = "VM \"Windows\" has been successfully started."
    command = """VBoxManage startvm %s 
    """ % (VM_NAME)
    response = os.popen(command).read()
    print("Waiting loop")
    while ("started" not in response):
        time.sleep(1)
    print("Response:\n",response)
    print("Done")

def waitForExecutionService():
    print("Waiting 30")
    time.sleep(30)
    print("Waiting done")

def powerOffVM():
    print("Powering off VM")
    command = "VBoxManage controlvm \"%s\" poweroff" % (VM_NAME)
    # print("Command to execute:\n", command)
    response = os.popen(command).read()
    print(response)

def restoreVM(snapshot):
    print("Restoring VM")
    command = "VBoxManage snapshot \"%s\" restore \"%s\"" % (VM_NAME, snapshot)
    # print("Command to execute:\n", command)
    response = os.popen(command).read()
    waitForExecutionService()
    print(response)

# This method should power off the VM, restore the vM to its
# Uninfected state, and then launch it again
def cycleVM():
    powerOffVM()
    restoreVM(VM_SNAPSHOT)
    launchVM()
    print("VM has been cycled, ready for a new sample")

