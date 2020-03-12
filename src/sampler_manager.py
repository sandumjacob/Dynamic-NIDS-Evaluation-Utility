# This Python script runs on the machine with which the sampling
# should be controlled from. It acts a server that the samplers connect
# to and sends signals to the samplers.

import socket
import server_config
from threading import Thread

# For manual control of sampling from the SamplerManager
console_enabled = False


class ClientThread(Thread):
    ready = False

    def __init__(self, ip):
        Thread.__init__(self)
        self.ip = ip
        self.port = PORT
        print("New thread started for " + ip)

    def run(self):
        print("Thread started")

    # The argument origin dictates whether the sample
    # will be executed on this thread instance VM
    def signal_sampling(self, path, incubation_time, origin):
        self.ready = False
        if origin:
            message = ""
            if origin:
                message = "Sample%d: %s" % (incubation_time, path)
                print("Signal Message: %s" % (message))
            else:
                message = "Passive: "
            print("Sending message: \n%s\n To IP address: %s" % (message, ip))
            connection.send(message.encode())
            # connection.shutdown(0)
            print("Message Sent")
            while not self.ready:
                print("Waiting for ready")
                data = connection.recv(BUFFER_SIZE)
                string_data = data.decode()
                print("Sampler manager received messge:")
                print(string_data)
                if string_data == "Ready":
                    print("SM received ready")
                    self.ready = True


IP = server_config.SERVER_IP
PORT = server_config.SERVER_PORT
BUFFER_SIZE = server_config.SERVER_BUFFER_SIZE
CLIENT_COUNT = server_config.CLIENT_COUNT
serversocket = socket.socket(socket.AF_INET, socket.SOCK_STREAM)
serversocket.bind((IP, PORT))
threads = []

# Wait for connections from the samplers
while len(threads) < CLIENT_COUNT:
    serversocket.listen(5)
    connection, (ip, port) = serversocket.accept()
    newthread = ClientThread(ip)
    newthread.start()
    threads.append(newthread)

for t in threads:
    t.join()

print(t)


# This function is used to tell the network of VMs to execute
# a worm-type malware sample on an origin VM so that it can
# proliferate. A signal is sent to all the VMs, but only one
# is told to execute a sample.
def sampleAtOrigin(origin_ip, sample_path, incubation_time):
    for thread in threads:
        if thread.ip == origin_ip:
            # Execute sample at origin infection point of originIP
            thread.signal_sampling(sample_path, incubation_time, True)
        else:
            thread.signal_sampling(sample_path, False)
    # for thread in threads:
    #     while (not thread.ready):
    #         #Wait for all samplers to finish
    #         print("Waiting for ready")
        print("All ready")


# Will input a specific packet and send a signal to one of the VM machines to generate that packet locally
# Most likely to be in the form of a random packet pattern taken from a benign sample PCAP.
def injectPacket(origin_ip, packet):
    print("Injecting packet at %s", origin_ip)

# for x in range(500):
while console_enabled:
    # C:\\Program Files (x86)\\Internet Explorer\\iexplore.exe
    inputIP = input("Enter IP for sampling: ")
    inputPath = input("Enter Path of Executable: ")
    input_incubation_time = int(input("Enter incubation time"))
    sampleAtOrigin(inputIP, inputPath, input_incubation_time)
    # threads[0].signalSampling(inputPath, True)

# while not console_enabled:
#     print("Automatic execution here")
# serversocket.close()