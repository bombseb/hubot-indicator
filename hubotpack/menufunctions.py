# -*- coding: utf-8 -*-
import os
import gi
from .PrefsWindow import *
gi.require_version('Gtk', '3.0')
from gi.repository import Gtk as gtk


class appMenu(gtk.Menu):
	def __init__(self):
	    gtk.Menu.__init__ (self)

	    item = gtk.MenuItem('Status : Unknown', name='status')
	    item.set_sensitive (False)
	    self.append(item)

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

	    self.show_all()

	def prefs(self, menuItem):
		PrefsWindow ()

	def pause(self, menuItem):
		os.system ("hubic pause")

		menuItem.set_label ("Enlever la pause")
		menuItem.disconnect(self.pauseResume_handler_ID)
		self.pauseResume_handler_ID = menuItem.connect ('activate', self.resume)

	def resume(self, menuItem):
		os.system ("hubic resume")

		menuItem.set_label ("Mettre en pause")
		menuItem.disconnect(self.pauseResume_handler_ID)
		self.pauseResume_handler_ID = menuItem.connect ('activate', self.pause)

	def synchro(self, menuItem):
		os.system ("hubic synchronize")

	def quit(self, menuItem):
		gtk.main_quit()
