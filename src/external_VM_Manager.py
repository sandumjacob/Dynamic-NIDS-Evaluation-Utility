import subprocess, os, time
import client_config as client_config
# A library for integrating VBoxManage Bash scripting
# into Python 

VM_NAME = client_config.VM_NAME
VM_USERNAME = client_config.VM_USERNAME
VM_PASSWORD = client_config.VM_PASSWORD
VM_SNAPSHOT = client_config.VM_SNAPSHOT

VM_CMD_PATH = "c:\\windows\\system32\\cmd.exe"


def hook_vm_cmd(filePath):
    command = "VBoxManage --nologo guestcontrol \"%s\" run --exe \"%s\" --username %s --password %s --wait-stdout" % (VM_NAME, VM_CMD_PATH, VM_USERNAME, VM_PASSWORD)

    print("Command to execute:\n", command)
    stream = os.popen(command, mode='w')
    print("Response: ", stream)
    # subprocess.run([command, "-1"])


def execute_file_in_vm(filepath):
    command = "VBoxManage --nologo guestcontrol \"%s\" run --exe \"%s\" --username %s --password %s --wait-stdout" % (VM_NAME, filepath, VM_USERNAME, VM_PASSWORD)
    print("Command to execute:\n", command)
    stream = os.popen(command)
    print("Response: ", stream)


def list_running_vms():
    command = "VBoxManage list runningvms" 
    print(os.system)


def launch_vm():
    success = "VM \"Windows\" has been successfully started."
    command = """VBoxManage startvm %s 
    """ % (VM_NAME)
    response = os.popen(command).read()
    print("Waiting loop")
    while "started" not in response:
        time.sleep(1)
    print("Response:\n",response)
    print("Done")


def wait_for_execution_service():
    print("Waiting 30")
    time.sleep(30)
    print("Waiting done")


def power_off_vm():
    print("Powering off VM")
    command = "VBoxManage controlvm \"%s\" poweroff" % VM_NAME
    # print("Command to execute:\n", command)
    response = os.popen(command).read()
    print(response)


def restore_vm():
    print("Restoring VM")
    command = "VBoxManage snapshot \"%s\" restore \"%s\"" % (VM_NAME, VM_SNAPSHOT)
    # print("Command to execute:\n", command)
    response = os.popen(command).read()
    print(response)
    time.sleep(1)


# This method should power off the VM, restore the vM to its
# Uninfected state, and then launch it again
def cycle_vm():
    power_off_vm()
    restore_vm()
    # waitForExecutionService()
    launch_vm()
    print("VM has been cycled, ready for a new sample")

