# -*- coding: utf-8 -*-
import os
from .vars import *
import dbus

class HubicBackup:
	def __init__(self, backupName):
		self.backupName = backupName

		# Doc Hubic DBus : /usr/share/doc/hubic/dbusapi/index.html#gdbus-com.hubic.backup
		self.backup = SESSION_BUS.get_object(BUSNAME, '/com/hubic/Backup/' + backupName)

	def getName (self):
		return self.backup.Get('com.hubic.backup', 'Name')

	def getOwned (self):
		return self.backup.Get('com.hubic.backup', 'Owned')

	def getLastBackup (self):
		return self.backup.Get('com.hubic.backup', 'LastBackup')

	def getSize (self):
		return self.backup.Get('com.hubic.backup', 'Size')

	def getLocalPath (self):
		return self.backup.Get('com.hubic.backup', 'LocalPath')

	# def _setLocalPath (self, val):
	# 	self.backup.Set ('com.hubic.backup', 'LocalPath', val)

	def getBackupInProgress (self):
		return self.backup.Get('com.hubic.backup', 'BackupInProgress')

	def getFrequency (self):
		return self.backup.Get('com.hubic.backup', 'Frequency').lower ()

	def getDeletePolicy (self):
		return self.backup.Get('com.hubic.backup', 'DeletePolicy').lower ()

	def getVersionsKept (self):
		return self.backup.Get('com.hubic.backup', 'VersionsKept')

	# def _setVersionsKept (self, val):
	# 	print ("setVersionKept = " + str (val))
	# 	self.backup.Set ('com.hubic.backup', 'VersionsKept', val)


	# localPath = property(_getLocalPath, _setLocalPath)
	# versionsKept = property (_getVersionsKept, _setVersionsKept)

