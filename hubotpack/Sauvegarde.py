# -*- coding: utf-8 -*-
import os
import gi
from .functions import *
gi.require_version('Gtk', '3.0')
from gi.repository import Gtk as gtk

import dbus
from .HubicBackup import *

class Sauvegarde:
	def __init__(self, parent, iterSauvegarde):
		builder = gtk.Builder()
		builder.add_from_file(os.path.join ('gui', 'sauvegarde.glade'))  # Rentrez évidemment votre fichier, pas le miens!

		self.parent 	= parent
		self.name		= self.parent.treestore_sauvegardes.get_value (iterSauvegarde, 1)
		self.localPath 	= self.parent.treestore_sauvegardes.get_value (iterSauvegarde, 2)
		self.lastBackup = self.parent.treestore_sauvegardes.get_value (iterSauvegarde, 3)
		self.size 		= self.parent.treestore_sauvegardes.get_value (iterSauvegarde, 4)

		for o in builder.get_objects():
			if issubclass(type(o), gtk.Buildable):
				objName = gtk.Buildable.get_name(o)
				setattr(self, objName, o)

		builder.connect_signals (self)

		self.backup = HubicBackup (self.name)
		self.comboboxtext_frequency.set_active_id (self.backup.getFrequency ())
		self.switch_keepdeleted.set_state (self.backup.getDeletePolicy () == 'keep')
		self.spinbutton_versionskept.set_value (self.backup.getVersionsKept ())

		self.window_sauvegarde.set_title ("Sauvegarde : {} ".format (self.name))
		self.filechooserbutton_localpath.set_filename (self.localPath)
		self.label_name.set_label (self.name)
		self.label_lastbackup.set_label (self.lastBackup)
		self.label_size.set_label (convert_size (self.backup.getSize ()))
		self.window_sauvegarde.show_all()



		# ---- DBUS ----
		# DBusGMainLoop(set_as_default=True)
        # self.on_state_change(self.hubic_state, 'Starting')
        # dbus.SystemBus().add_signal_receiver(self.on_networking_change, dbus_interface = 'org.freedesktop.NetworkManager', signal_name = 'StateChanged')
		#self.session_bus = dbus.SessionBus()
        # self.session_bus.add_signal_receiver(self.on_file_change, dbus_interface = 'com.hubic.account', signal_name = 'ItemChanged')
        # self.session_bus.add_signal_receiver(self.on_state_change, dbus_interface = 'com.hubic.general', signal_name = 'StateChanged')
        # self.session_bus.add_signal_receiver(self.on_message, dbus_interface = 'com.hubic.general', signal_name = 'Messages')
        # self.session_bus.call_on_disconnection(self.cleanup_dbus_infos)

        # self.hubic_account_obj = self.session_bus.get_object('com.hubiC', '/com/hubic/Account')
        # self.hubic_account_iface = dbus.Interface(self.hubic_account_obj, 'com.hubic.account')
        # self.hubic_general_obj = self.session_bus.get_object('com.hubiC', '/com/hubic/General')
        # self.hubic_general_iface = dbus.Interface(self.hubic_general_obj, 'com.hubic.general')

        # self.ff_helper.set_hubic_dir(self.get_hubic_dir())
        # self.encfs_menu.set_hubic_dir(self.get_hubic_dir())
        # self.on_state_change('Starting', self.hubic_general_obj.Get('com.hubic.general', 'CurrentState'))


	def on_button_annuler_clicked (self, button):
		self.window_sauvegarde.close ()
		# h = HubicBackup ("SaveMusic")
		# h.versionsKept = 12


