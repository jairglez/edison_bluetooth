#!/usr/bin/python

from optparse import OptionParser, make_option
import os, sys, socket, uuid, dbus, dbus.service, dbus.mainloop.glib
try:
  from gi.repository import GObject
except ImportError:
  import gobject as GObject

BUS_NAME = 'org.bluez'
AGENT_INTERFACE = 'org.bluez.Agent1'
AGENT_PATH = "/test/agent"

class Agent(dbus.service.Object):
        @dbus.service.method(AGENT_INTERFACE,                                                        in_signature="ou", out_signature="")
        def RequestConfirmation(self, device, passkey):
            print("RequestConfirmation (%s, %06d)" % (device, passkey))
            set_trusted(device)
            return
        def set_trusted(path):
            props = dbus.Interface(bus.get_object("org.bluez", path), 
                                            "org.freedesktop.DBUs.Properties")
            props.Set("org.bluez.Device1", "Trusted", True)

class Profile(dbus.service.Object):
	fd = -1
	@dbus.service.method("org.bluez.Profile1",
				in_signature="oha{sv}", out_signature="")
	def NewConnection(self, path, fd, properties):
		self.fd = fd.take()
		print("\nConnected to (%s, %d)" % (path, self.fd))

		server_sock = socket.fromfd(self.fd, socket.AF_UNIX, socket.SOCK_STREAM)
		server_sock.setblocking(1)
		server_sock.send("Hello, this is Edison!")
		try:
		    while True:
		        data = server_sock.recv(1024)
		        print("Smartphone says: %s" % data)
			server_sock.send("Edison received: %s\n" % data)
		except IOError:
		    pass

		server_sock.close()
		print("Disconnected")

if __name__ == '__main__':
        
        # Generic dbus config
        dbus.mainloop.glib.DBusGMainLoop(set_as_default=True)
	bus = dbus.SystemBus()

        #Profile config
	profile_manager = dbus.Interface(bus.get_object("org.bluez",
				"/org/bluez"), "org.bluez.ProfileManager1")	        profile_path = "/foo/bar/profile"
        auto_connect = {"AutoConnect": False}
        profile_uuid = "1101"
	profile = Profile(bus, proile_path)
	manager.RegisterProfile(profile_path, profile_uuid, auto_connect)
   
        # Agent config
        agent_manager = dbus.Interface(bus.get_object("org.bluez",
				"/org/bluez"), "org.bluez.AgentManager1")
        agent_path = "/test/agent"
        agent = Agent(bus, agent_path)
        agent_capability = "KeyboardDisplay"
        agent_manager = dbus.Interface(obj, "org.bluez.AgentManager1")
        agent_manager.RegisterAgent(agent_path, agent_capability)

        # Mainloop
	mainloop = GObject.MainLoop()
	mainloop.run()