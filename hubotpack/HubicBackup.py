# -*- coding: utf-8 -*-
import os
from .vars import *
import dbus

class HubicBackup:
	def __init__(self, backupName):
		self.backupName = backupName

		# Doc Hubic DBus : /usr/share/doc/hubic/dbusapi/index.html#gdbus-com.hubic.backup
		self.backup = SESSION_BUS.get_object(BUSNAME, '/com/hubic/Backup/' + self.backupName)

	def delete (self):
		self.backup.Delete ()

	def backupNow (self):
		self.backup.BackupNow ()

	def downloadInto (self, path):
		self.backup.DownloadInto (path)

	def attachToThisComputer (self, path):
		self.backup.AttachToThisComputer (path)

	def getPropertie (self, propName):
		return self.backup.Get('com.hubic.backup', propName)

	def setPropertie (self, propName, val):
		if propName == 'DeletePolicy':
			if val:
				val = 'keep'
			else:
				val = 'delete'

		self.backup.Set ('com.hubic.backup', propName, val, dbus_interface='org.freedesktop.DBus.Properties')

