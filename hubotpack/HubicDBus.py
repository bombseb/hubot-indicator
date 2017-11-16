# -*- coding: utf-8 -*-
import os
from .vars import *
import dbus
from dbus.mainloop.glib import DBusGMainLoop


BUSNAME = 'com.hubiC'
DBusGMainLoop(set_as_default=True)
SESSION_BUS = dbus.SessionBus()


class HubicDBus:
	def __init__ (self, api, objName):
		# Doc Hubic DBus : /usr/share/doc/hubic/dbusapi/index.html
		self.dbusObj = SESSION_BUS.get_object(BUSNAME, '/com/hubic/' + objName)
		self.api = api

	def getProperty (self, propName):
		return self.dbusObj.Get(self.api, propName)

	def setProperty (self, propName, val):
		self.dbusObj.Set (self.api, propName, val, dbus_interface='org.freedesktop.DBus.Properties')

	def addCallBack (self, function, signal_name):
		SESSION_BUS.add_signal_receiver(function, dbus_interface = self.api, signal_name = signal_name)



class HubicBackup(HubicDBus):
	def __init__(self, backupName):
		HubicDBus.__init__(self, 'com.hubic.backup', 'Backup/' + backupName)

	def delete (self):
		self.dbusObj.Delete ()

	def backupNow (self):
		self.dbusObj.BackupNow ()

	def downloadInto (self, path):
		self.dbusObj.DownloadInto (path)

	def attachToThisComputer (self, path):
		self.dbusObj.AttachToThisComputer (path)



class HubicAccount(HubicDBus):
	def __init__(self):
		HubicDBus.__init__(self, 'com.hubic.account', 'Account')

	def setPauseState(self, state):
		self.dbusObj.SetPauseState (state)

	def synchronizeNow (self):
		self.dbusObj.SynchronizeNow ()

	def createBackup (self, path, name, frequency, versionsKept, keepDeletedFiles):
		self.dbusObj.CreateBackup (path, name, frequency, versionsKept, keepDeletedFiles)

	def logout (self):
		self.dbusObj.Logout ()

class HubicGeneral(HubicDBus):
	def __init__(self):
		HubicDBus.__init__(self, 'com.hubic.general', 'General')

	def login (self, email, password, synchronizedDir):
		self.dbusObj.Login (email, password, synchronizedDir)


class HubicSettings(HubicDBus):
	def __init__(self):
		HubicDBus.__init__(self, 'com.hubic.settings', 'Settings')

	def setAuthenticatedProxy(self, hostName, port, userName, password):
		self.dbusObj.SetAuthenticatedProxy (hostName, port, userName, password)

	def setProxy(self, hostName, port):
		self.dbusObj.SetProxy (hostName, port)

	def unsetProxy(self):
		self.dbusObj.UnsetProxy ()

