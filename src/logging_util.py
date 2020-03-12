# TODO: Improve logging utilities
import csv, os, numpy, threading
import client_config as client_config
from scapy.all import *

# This works for now but I will probably need to 
# implement a storage cache to avoid rampant 
# memory usage
EXPORT_DIR = client_config.EXPORT_DIR
logged_packets = []
interface = client_config.INTERFACE
t = AsyncSniffer(iface=interface)


# Captures packets indefinitely
def live_capture_for_packet_count(packet_count):
    sniff(iface=interface, prn=lambda x: log_packet(x), count=packet_count)


def recv_packet_callback(packet):
    print("Packet intercepted: \n%s" % packet)
    log_packet(packet)


# Captures packets as long as the boolean argument
# stopcondition is True. 
def async_packet_capture(stop_condition):
    t.start()
    while True:
        if stop_condition:
            t.stop()
            for result in t.results:
                log_packet(result)
            break


# Captures packets for x seconds in a synchronous manner
def sync_packet_capture_for(seconds):
    print("Capturing packets...")
    t.start()
    time.sleep(float(seconds))
    t.stop()
    for result in t.results:
        log_packet(result)
    print("Done capturing packets")


# Captures packets for x seconds in an asynchronous manner
# Since it is asynchronous, the boolean argument
# export can be used to specify an automatic export
# at the end of execution
def async_packet_capture_for(seconds, export, wipe):
    print("Capturing packets...")
    # This executes once seconds has passed

    def done():
        print("Done capturing packets")
        t.stop()
        for result in t.results:
            log_packet(result)
        if export:
            export_packet_log(True)

    timer = threading.Timer(seconds, done)
    t.start()
    timer.start()


# Exports the logged packets to a pcap file
# with a date-time filename
def export_packet_log(wipe):
    print("Exporting packet logs")
    filename = "Capture: %s" % (time.strftime("%Y%m%d-%H%M%S"))
    export_path = os.path.join(EXPORT_DIR, filename)
    wrpcap(export_path, logged_packets)
    if wipe:
        wipe_log()


# Exports the logged packets to a pcap file
# with a specified filename
def export_packet_log_with_name(filename, wipe):
    print("Exporting packet logs")
    print(logged_packets)
    export_path = os.path.join(EXPORT_DIR, filename)
    wrpcap(export_path, logged_packets)
    if wipe:
        wipe_log()


def live_capture_with_callback_on_condition(condition):
    while condition:
        live_capture_with_callback(recv_packet_callback)


def live_capture_with_callback(callback):
    sniff(iface=interface, prn=callback)


# Automatically determines whether to cache or continue
# in memory
def log_packet(packet):
    logged_packets.append(packet)


# Wipe cache and memory
def wipe_log():
    logged_packets.clear()
