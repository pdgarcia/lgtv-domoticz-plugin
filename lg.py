#from pylgtv import WebOsClient

import sys
import logging
import argparse
import socket
import struct
import asyncio
import http.client
import xml.etree.ElementTree as etree
lgtv = {}
headers = {"Content-Type": "application/atom+xml"}

logging.basicConfig(filename='lgtv-error.log', level=logging.ERROR, format='%(asctime)s %(levelname)s %(name)s %(message)s')

class LgCommand (object):
    def __init__(self, ip):
        lgtv["ipaddress"] = ip
        lgtv["pairingKey"] = "285540"
        #self.client = WebOsClient(ip)

        self.commandLines = {
            'off': self.off,
            'on': self.wakeonlan,
            'software-info': self.software_info,
            'volume-up': self.volume_up,
            'volume-down': self.volume_down,
            'current-app': self.current_app,
            'apps': self.apps,
            'services': self.services,
            'get-volume': self.get_volume,
            'get-inputs': self.get_inputs,
            'app': self.app,
            'set-volume': self.set_volume,
            'close-app': self.close_app,
            'mute': self.mute,
            'unmute': self.unmute,
            'get-mute': self.get_mute,
            'get-input': self.get_input,
            'set-input': self.set_input,
            'channel-up': self.channel_up,
            'channel-down': self.channel_down,
            'channels': self.channels,
            'get-channel': self.get_channel,
            'info': self.info,
            'set-channel': self.set_channel,

            'play': self.play,
            'pause': self.pause,
            'stop': self.stop,
            'close': self.close,
            'rewind': self.rewind,
            'fast-forward': self.fast_forward,

            'enter': self.enter,
            'delete': self.delete,

            #'3d-on': threeDOn,
            #'3d-off': threeDOff,
        }

    def run(self, command, arg=None):
        return self.commandLines[command](arg);

    def delete(self, arg):
        print("delete")
        #return self.client.send_delete_key()

    def enter(self, arg):
        print("enter")
        #return self.client.send_enter_key()

    def play(self, arg):
        print("play")
        #return self.client.play()

    def pause(self, arg):
        print("pause")
        #return self.client.pause()

    def stop(self, arg):
        print("stop")
        #return self.client.stop()

    def close(self, arg):
        print("close")
        #return self.client.close()

    def rewind(self, arg):
        print("rewind")
        #return self.client.rewind()

    def fast_forward(self, arg):
        print("fast_forward")
        #return self.client.fast_forward()

    def info(self, arg):
        print("info")
        #return self.client.get_channel_info()

    def set_channel(self, arg):
        print("set_channel")
        #return self.client.set_channel(arg)

    def get_channel(self, arg):
        print("get_channel")
        return (self.sendCommand("45"))

    def channels(self, arg):
        print("channels")
        #return self.client.get_channels()

    def channel_down(self, arg):
        print("channel_down")
        return self.sendCommand("28")

    def channel_up(self, arg):
        print("channel_up")
        return self.sendCommand("27")

    def get_input(self, arg):
        print("get_input")
        #return self.client.get_input()

    def set_input(self, arg):
        print("set_input")
        #return self.client.set_input(arg)

    def unmute(self, arg):
        print("unmute")
        return self.sendCommand("26")

    def mute(self, arg):
        print("mute")
        return self.sendCommand("26")

    def get_mute(self, arg):
        print("get_mute")
        #return self.client.get_muted()

    def set_volume(self, arg):
        print("set_volume")
        #return self.client.set_volume(int(arg))

    def close_app(self, arg):
        print("close_app")
        #return self.client.close_app(arg)

    def app(self, arg):
        print("app")
        #return self.client.launch_app(arg)

    def get_inputs(self, arg):
        print("get_inputs")
        #return self.client.get_inputs()

    def get_volume(self, arg):
        print("get_volume")
        #return self.client.get_volume()

    def services(self, arg):
        print("services")
        #return self.client.get_services()

    def current_app(self, arg):
        print("current_app")
        #return self.client.get_current_app()

    def apps(self, arg):
        print("apps")
        #return self.client.get_apps()

    def off(self, arg):
        #self.client.power_off()
        return "TV has been turned off."

    def software_info(self, arg):
        print("software_info")
        #return self.check()

    def volume_down(self, arg):
        print("volume_down")
        #return self.client.volume_down()

    def volume_up(self, arg):
        print("volume_up")
        #return self.client.volume_up()

    def wakeonlan(self, mac):
        if mac is not None:
            addr_byte = mac.split(':')
            hw_addr = struct.pack('BBBBBB', int(addr_byte[0], 16),
                                  int(addr_byte[1], 16),
                                  int(addr_byte[2], 16),
                                  int(addr_byte[3], 16),
                                  int(addr_byte[4], 16),
                                  int(addr_byte[5], 16))
            msg = b'\xff' * 6 + hw_addr * 16
            socket_instance = socket.socket(socket.AF_INET, socket.SOCK_DGRAM)
            socket_instance.setsockopt(socket.SOL_SOCKET, socket.SO_BROADCAST, 1)
            socket_instance.sendto(msg, ('<broadcast>', 9))
            socket_instance.close()
            return "TV has been turned on."
        else:
            return "mac address (arg) not set. use -h for help."

    def check(self):
        print("check")
        #return self.client.get_software_info()
##############################################

    def displayKey(self):
        conn = http.client.HTTPConnection( lgtv["ipaddress"], port=8080)
        reqKey = "<?xml version=\"1.0\" encoding=\"utf-8\"?><auth><type>AuthKeyReq</type></auth>"
        conn.request("POST", "/roap/api/auth", reqKey, headers=headers)
        httpResponse = conn.getresponse()
        if httpResponse.reason != "OK" : sys.exit("Network error")
        return httpResponse.reason

    def getSessionid(self):
        conn = http.client.HTTPConnection( lgtv["ipaddress"], port=8080)
        pairCmd = "<?xml version=\"1.0\" encoding=\"utf-8\"?><auth><type>AuthReq</type><value>" \
                + lgtv["pairingKey"] + "</value></auth>"
        conn.request("POST", "/roap/api/auth", pairCmd, headers=headers)
        httpResponse = conn.getresponse()
        if httpResponse.reason != "OK" : return httpResponse.reason
        tree = etree.XML(httpResponse.read())
        return tree.find('session').text

    def handleCommand(self,cmdcode):
        conn = http.client.HTTPConnection( lgtv["ipaddress"], port=8080)
        cmdText = "<?xml version=\"1.0\" encoding=\"utf-8\"?><command>" \
                   + "<name>HandleKeyInput</name><value>" \
                   + cmdcode \
                   + "</value></command>"
        conn.request("POST", "/roap/api/command", cmdText, headers=headers)
        httpResponse = conn.getresponse()
        return etree.XML(httpResponse.read())

    def sendCommand(self,cmd):
        theSessionid = self.getSessionid()
        if len(theSessionid) < 8 : logging.exception("Oops: Could not get Session Id: " + theSessionid)
        lgtv["session"] = theSessionid
        return self.handleCommand(cmd)

#############################################
def main():
    parser = argparse.ArgumentParser()
    parser.add_argument("ip", help="ip address of the tv")

    parser.add_argument("-c", "--command", help="the command to run", default='')
    parser.add_argument("-a", "--arg", help="command argument", default=None)
    args = parser.parse_args()

    cmd = LgCommand(args.ip)
    if(args.command):
        logging.info("Running Command: " + args.command)
        print(cmd.run(args.command, args.arg))
    else:
        cmd.check()
        print("TV is on.")

try:
    main()
except asyncio.TimeoutError as te:
    print("TimeoutError() occurred, is the TV off? ")
except:
    logging.exception("Oops:")
    print (sys.exc_info())
