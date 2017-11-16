# -*- coding: utf-8 -*-
import os
import gi
from .vars import *
from .functions import *
gi.require_version('Gtk', '3.0')
from gi.repository import Gtk as gtk, Gdk as gdk, GObject
from .HubicDBus import * 


class LoginWindow:
	def __init__(self, afficheInfos):
		builder = gtk.Builder()
		builder.add_from_file(os.path.join ('gui', 'login.glade'))  # Rentrez évidemment votre fichier, pas le miens!

		self.afficheInfos = afficheInfos
		self.window = builder.get_object ('window_login')
		self.entry_mail = builder.get_object('entry_mail')
		self.entry_pass = builder.get_object('entry_pass')
		self.button_connexion = builder.get_object('button_connexion')
		self.password_path = os.path.join (APPDIR, 'hubicpasswd')

		# Le handler
		handler = {'on_button_connexion_clicked' : self.on_button_connexion_clicked, 
					'on_button_annuler_clicked' : self.on_button_annuler_clicked,
					'on_window_login_delete_event' : self.on_window_login_delete_event}
		builder.connect_signals(handler)

		self.window.show_all()

	def _set_busy_cursor(self, busy):
		cursor = None

		if busy:
			cursor = gdk.Cursor(gdk.CursorType.WATCH)
		else:
			cursor = gdk.Cursor(gdk.CursorType.LEFT_PTR)

		gdk_window = self.window.get_window()
		gdk_window.set_cursor(cursor)


	def login (self):
		email = self.entry_mail.get_text ()
		passwd = self.entry_pass.get_text ()

		try:
			hubicGeneral.login (email, passwd, '')
		except dbus.exceptions.DBusException as e:
			messageBox (self.window, e.get_dbus_message (), messageType=gtk.MessageType.ERROR)

		self.afficheInfos ()
		self._set_busy_cursor(False)

		self.window.close ()

	def on_button_connexion_clicked (self, button):
		self._set_busy_cursor(True)
		GObject.idle_add(self.login)


	def on_button_annuler_clicked (self, button):
		self.window.close ()

	def on_window_login_delete_event (self, widget, event):
		try:
			os.remove (os.path.join (APPDIR, '.hubicpasswd'))
		except FileNotFoundError:
			pass


		
