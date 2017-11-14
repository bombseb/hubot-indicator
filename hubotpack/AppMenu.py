# -*- coding: utf-8 -*-
import os
import gi
from .PrefsWindow import *
gi.require_version('Gtk', '3.0')
from gi.repository import Gtk as gtk
from .vars import *


class AppMenu(gtk.Menu):
	def __init__(self, indicator):
		gtk.Menu.__init__ (self)

		self.indicator = indicator

		self.itemStatus = gtk.MenuItem('Status : Unknown', name='status')
		self.itemStatus.set_sensitive (False)
		self.append(self.itemStatus)

		item = gtk.MenuItem('Mettre en pause', name='pauseresume')
		self.pauseResume_handler_ID = item.connect('activate', self.pause)
		self.append(item)

		item = gtk.MenuItem('Synchroniser maintenant', name='synchro')
		item.connect('activate', self.synchro)
		self.append(item)

		item = gtk.MenuItem('Préférences')
		item.connect('activate', self.prefs)
		self.append(item)

		item = gtk.MenuItem('Quit')
		item.connect('activate', self.quit)
		self.append(item)

		self.hubicGeneral = SESSION_BUS.get_object(BUSNAME, '/com/hubic/General')
		s = self.hubicGeneral.Get('com.hubic.general', 'CurrentState')
		self.on_state_changed (None, s)
		SESSION_BUS.add_signal_receiver(self.on_state_changed, dbus_interface = 'com.hubic.general', signal_name = 'StateChanged')

		self.hubicAccount = SESSION_BUS.get_object(BUSNAME, '/com/hubic/Account')
		self.hubicAccountIFace = dbus.Interface(self.hubicAccount, 'com.hubic.account')

		self.show_all()

	def prefs(self, menuItem):
		PrefsWindow ()

	def pause(self, menuItem):
		self.hubicAccountIFace.SetPauseState (True)

		menuItem.set_label ("Enlever la pause")
		menuItem.disconnect(self.pauseResume_handler_ID)
		self.pauseResume_handler_ID = menuItem.connect ('activate', self.resume)

	def resume(self, menuItem):
		self.hubicAccountIFace.SetPauseState (False)

		menuItem.set_label ("Mettre en pause")
		menuItem.disconnect(self.pauseResume_handler_ID)
		self.pauseResume_handler_ID = menuItem.connect ('activate', self.pause)

	def synchro(self, menuItem):
		self.hubicAccountIFace.SynchronizeNow ()

	def quit(self, menuItem):
		gtk.main_quit()

	def on_state_changed (self, oldState, newState):
		# NotConnected: Client is not connected to an account
		# Connecting: Connection is in progress
		# Paused: Client is in pause, no synchronization will occur
		# Idle: Connected, watching for changes and wait for next sync
		# Busy: Connected and currently index/synchronize content

		self.itemStatus.set_label ("Status : {}".format (newState))

		if newState == "Idle":
			self.indicator.set_icon (ICON_OK)
		elif newState == "Paused":
			self.indicator.set_icon (ICON_OK)
		elif newState == "Busy":
			self.indicator.set_icon (ICON_BUSY)
		elif newState in ("Unknown", "NotConnected", "Connecting"):
			self.indicator.set_icon (ICON_ERROR)
		else:
			self.indicator.set_icon (ICON_ERROR)

	def __del__ (self):
		SESSION_BUS.remove_signal_receiver(self.on_state_changed, dbus_interface = 'com.hubic.general', signal_name = 'StateChanged')
