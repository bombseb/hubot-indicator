# -*- coding: utf-8 -*-
# Copyright (C) 2017 Bombasaro Sébastien
# bombseb@gmail.Com
# https://github.com/bombseb/hubot-indicator
#
# This program is free software; you can redistribute it and/or modify
# it under the terms of the GNU General Public License as published by
# the Free Software Foundation; either version 2 of the License, or
# (at your option) any later version.
#
# This program is distributed in the hope that it will be useful,
# but WITHOUT ANY WARRANTY; without even the implied warranty of
# MERCHANTABILITY or FITNESS FOR A PARTICULAR PURPOSE. See the
# GNU General Public License for more details.
#
# You should have received a copy of the GNU General Public License along
# with this program; if not, write to the Free Software Foundation, Inc.,
# 51 Franklin Street, Fifth Floor, Boston, MA 02110-1301 USA.

import os
import gi
from hubotpack.PrefsWindow import *
from hubotpack.variables import *
from hubotpack.HubicDBus import *
from hubotpack.functions import *
from hubotpack.RunningOperations import *
gi.require_version('Gtk', '3.0')
from gi.repository import Gtk as gtk, GdkPixbuf

class AppMenu(gtk.Menu):
	def __init__(self, indicator):
		gtk.Menu.__init__ (self)

		self.indicator = indicator

		self.itemStatus = gtk.MenuItem('Status : Unknown')
		self.itemStatus.set_sensitive (False)
		self.append(self.itemStatus)

		self.append(gtk.SeparatorMenuItem())

		self.item_pauseResume = gtk.MenuItem('Mettre en pause')
		self.pauseResume_handler_ID = self.item_pauseResume.connect('activate', self.pause)
		self.append(self.item_pauseResume)

		self.item_synchro = gtk.MenuItem('Synchroniser maintenant')
		self.item_synchro.connect('activate', self.synchro)
		self.append(self.item_synchro)

		item = gtk.ImageMenuItem ('Préférences')
		# item.set_image(gtk.Image.new_from_file(ICON_ERROR))
		item.set_always_show_image(True)
		item.connect('activate', self.prefs)
		self.append(item)

		item = gtk.MenuItem('Voir les opérations en cours')
		item.connect('activate', self.runningOperations)
		self.append(item)

		self.append(gtk.SeparatorMenuItem())

		item = gtk.MenuItem('A propos')
		item.connect('activate', self.aPropos)
		self.append(item)

		item = gtk.MenuItem('Quitter')
		item.connect('activate', self.quit)
		self.append(item)

		s = hubicGeneral.getProperty ('CurrentState')
		self.on_state_changed (None, s)
		hubicGeneral.addCallBack (self.on_state_changed, 'StateChanged')

		self.show_all()

	def prefs(self, menuItem):

		try:
			self.prefsWindow.window_prefs.present ()
		except AttributeError:
			self.prefsWindow = PrefsWindow (self)

	def runningOperations(self, menuItem):
		r = RunningOperations ()
		# r.run ()
		# r.destroy()

	def pause(self, menuItem):
		hubicAccount.setPauseState (True)

	def resume(self, menuItem):
		hubicAccount.setPauseState (False)

	def synchro(self, menuItem):
		hubicAccount.synchronizeNow ()

	def aPropos(self, menuItem):
		builder = gtk.Builder()
		builder.add_from_file(os.path.join (APPDIR, 'gui', 'about.glade'))

		aboutDialog = builder.get_object("aboutdialog")
		aboutDialog.set_logo (GdkPixbuf.Pixbuf.new_from_file(ICON_IDLE))
		aboutDialog.set_version = VERSION
		aboutDialog.run()
		aboutDialog.destroy()

	def quit(self, menuItem):
		gtk.main_quit()

	def on_state_changed (self, oldState, newState):
		# NotConnected: Client is not connected to an account
		# Connecting: Connection is in progress
		# Paused: Client is in pause, no synchronization will occur
		# Idle: Connected, watching for changes and wait for next sync
		# Busy: Connected and currently index/synchronize content

		self.itemStatus.set_label ("Status : {}".format (newState))
		self.item_synchro.set_sensitive(newState != "Paused")

		if oldState != "Paused" and newState != oldState:
			self.item_pauseResume.set_label ("Mettre en pause")
			self.item_pauseResume.disconnect(self.pauseResume_handler_ID)
			self.pauseResume_handler_ID = self.item_pauseResume.connect ('activate', self.pause)

		if newState == "Idle":
			self.indicator.set_icon (ICON_IDLE)
		elif newState == "Paused":
			self.indicator.set_icon (ICON_PAUSE)

			self.item_pauseResume.set_label ("Enlever la pause")
			self.item_pauseResume.disconnect(self.pauseResume_handler_ID)
			self.pauseResume_handler_ID = self.item_pauseResume.connect ('activate', self.resume)

		elif newState == "Busy":
			self.indicator.set_icon (ICON_BUSY)
		elif newState in ("NotConnected", "Connecting"):
			self.indicator.set_icon (ICON_NOTCONNECTED)
		else:
			self.indicator.set_icon (ICON_ERROR)

	def __del__ (self):
		SESSION_BUS.remove_signal_receiver(self.on_state_changed, dbus_interface = 'com.hubic.general', signal_name = 'StateChanged')
