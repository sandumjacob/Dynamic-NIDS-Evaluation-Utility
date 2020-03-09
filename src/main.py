from random import randrange
import consolemenu as CM
from consolemenu import *
from consolemenu.items import *
from consolemenu.prompt_utils import PromptUtils
import config
import sampler_manager as sm
# C:\\Program Files (x86)\\Internet Explorer\\iexplore.exe

incubation_time=30
# Start SamplerServer
sm

def test_sample_on_network(sample): 
    # Find a random IP to execute the sample on
    # TODO: Fetch the ips automatically from the connected list
    x = randrange(3)
    # ip = config.machineIPs[x]
    # ip = '10.0.0.3'
    ip = '127.0.0.1'
    print("Random IP: " + ip)
    sm.sampleAtOrigin(ip, sample, incubation_time)
    screen = CM.Screen()
    PromptUtils(screen).enter_to_continue()
    

def test_sample_on_network_menu():
    sample = input("Enter name of sample on the sample server")
    path = "Y:\\Samples\\"
    test_sample_on_network(path+sample)


def test_sample_on_network_menu_path():
    sample = input("Enter path of the sample (VM-relative): ")
    test_sample_on_network(sample)

# Iterates through sample server to test all the samples in the Sample folder
def test_all_samples_in_sample_server():
    screen = CM.Screen()
    print("Testing all samples in the sample server")
    f = open("/root/Documents/paths.txt", "r")
    paths = f.readlines()
    print(paths)
    PromptUtils(screen).enter_to_continue()

# Diagnostic test
def open_ie_on_a_vm():
    x = input("Enter VM #")
    sm.threads[x].signalSampling("C:\\Program Files (x86)\\Internet Explorer\\iexplore.exe", True, incubation_time)

def open_settings():
    incubation_time = int(input("Enter incubation time for malware samples"))


menu = ConsoleMenu("Dynamic IDS Benchmark System")
menu_item_1 = FunctionItem("Test Individual Sample", test_sample_on_network_menu)
menu_item_2 = FunctionItem("Test All Samples", test_all_samples_in_sample_server)
menu_item_3 = FunctionItem('Test a sample at path', test_sample_on_network_menu_path)
menu_item_4 = FunctionItem("Open IE on VM", open_ie_on_a_vm)
menu_item_5 = FunctionItem("Settings", open_settings)
menu.append_item(menu_item_1)
menu.append_item(menu_item_2)
menu.append_item(menu_item_3)
menu.append_item(menu_item_4)
menu.append_item(menu_item_5)
menu.show()