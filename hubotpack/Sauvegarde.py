# -*- coding: utf-8 -*-
import os
import gi
from .functions import *
from .variables import *
gi.require_version('Gtk', '3.0')
from gi.repository import Gtk as gtk


class Sauvegarde:
	def __init__(self, parent, iterSauvegarde=None):
		builder = gtk.Builder()
		builder.add_from_file(os.path.join ('gui', 'sauvegarde.glade'))  # Rentrez évidemment votre fichier, pas le miens!

		self.parent 		= parent
		self.modifiedList 	= []
		self.iterSauvegarde = iterSauvegarde

		for o in builder.get_objects():
			if issubclass(type(o), gtk.Buildable):
				objName = gtk.Buildable.get_name(o)
				setattr(self, objName, o)

		builder.connect_signals (self)

		if iterSauvegarde == None:
			self.new = True
			self.entry_name.set_sensitive (True)
			self.label_lastbackup.set_label ('-')
			self.label_size.set_label ('-')

		else:
			self.new = False
			self.name		= self.parent.treestore_sauvegardes.get_value (iterSauvegarde, 1)
			self.localPath 	= self.parent.treestore_sauvegardes.get_value (iterSauvegarde, 2)
			self.lastBackup = self.parent.treestore_sauvegardes.get_value (iterSauvegarde, 3)
			self.size 		= self.parent.treestore_sauvegardes.get_value (iterSauvegarde, 4)

			self.backup = HubicBackup (self.name)
			self.comboboxtext_frequency.set_active_id (self.backup.getProperty ('Frequency'))

			self.switch_keepdeleted.set_state (self.backup.getProperty ('DeletePolicy').lower () == 'keep')
			self.spinbutton_versionskept.set_value (self.backup.getProperty ('VersionsKept'))
			self.window_sauvegarde.set_title ("Sauvegarde : {} ".format (self.name))
			self.filechooserbutton_localpath.set_filename (self.localPath)
			self.entry_name.set_text (self.name)
			self.entry_name.set_sensitive (False)
			self.label_lastbackup.set_label (self.lastBackup)
			self.label_size.set_label (convert_size (self.backup.getProperty ('Size')))
		
		self.modifiedList.clear ()

		self.window_sauvegarde.show_all()

	def on_modification (self, *args):
		self.modifiedList.append (args[0])

	def on_button_valider_clicked (self, button):
		path = self.filechooserbutton_localpath.get_filename ()
		name = self.entry_name.get_text ()
		frequency = self.comboboxtext_frequency.get_active_id()
		versionsKept = self.spinbutton_versionskept.get_value_as_int ()
		keepDeletedFiles = self.switch_keepdeleted.get_state ()

		if self.new:
			hubicAccount.createBackup (path, name, frequency, versionsKept, keepDeletedFiles)
			self.parent.treestore_sauvegardes.append(self.parent.iterCetOrdi, [True, name, path, '-', '-', True, False])

		else:
			if self.filechooserbutton_localpath in self.modifiedList:
				self.backup.setProperty ('LocalPath', path)
				self.parent.treestore_sauvegardes.set_value (self.iterSauvegarde, 2, path)

			if self.comboboxtext_frequency in self.modifiedList:
				self.backup.setProperty ('Frequency', frequency)

			if self.spinbutton_versionskept in self.modifiedList:
				self.backup.setProperty ('VersionsKept', versionsKept)

			if self.switch_keepdeleted in self.modifiedList:
				if keepDeletedFiles:
					keepDeletedFiles = 'keep'
				else:
					keepDeletedFiles = 'delete'
				self.backup.setProperty ('DeletePolicy', keepDeletedFiles)

		self.window_sauvegarde.close ()

	def on_button_annuler_clicked (self, button):
		self.window_sauvegarde.close ()


