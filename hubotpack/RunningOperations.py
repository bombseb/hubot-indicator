# -*- coding: utf-8 -*-
import os
import gi
from .vars import *
gi.require_version('Gtk', '3.0')
from gi.repository import Gtk as gtk, GObject

class RunningOperations:
	def __init__(self):
		builder = gtk.Builder()
		builder.add_from_file(os.path.join ('gui', 'runningoperations.glade'))

		for o in builder.get_objects():
			if issubclass(type(o), gtk.Buildable):
				name = gtk.Buildable.get_name(o)
				setattr(self, name, o)

		builder.connect_signals (self)

		self.window_running_operations.show_all()

		self.timeout_id = GObject.timeout_add(100, self.raffraichir)

		# self.raffraichir ()

	def raffraichir(self):
		result = hubicAccount.getProperty ('RunningOperations')

		if len (result) == 0: return True

		self.liststore_operations.clear ()

		for ligne in result:
			bytesDone = ligne[4]
			totalBytes = ligne[5]
			if totalBytes > 0:
				pourcentage = (bytesDone / totalBytes) * 100
			else:
				pourcentage = 0

			iterLigne = self.getIterFromID(ligne[0])

			if not iterLigne:
				self.liststore_operations.append ([ligne[0], ligne[1], ligne[2], ligne[3], bytesDone, totalBytes, pourcentage])
			else:
				if bytesDone > 0: self.liststore_operations.set_value(iterLigne, 4, bytesDone)
				if totalBytes > 0: self.liststore_operations.set_value(iterLigne, 5, totalBytes)
				if bytesDone > 0 and totalBytes > 0: self.liststore_operations.set_value(iterLigne, 6, pourcentage)

		return True

	def getIterFromID (self, idOp):
		# treeiter = modele.get_iter('0')
		treeiter = self.liststore_operations.get_iter_first()
		while treeiter:
			tmpID = self.liststore_operations.get_value (treeiter, 0)
			if tmpID == idOp:
				return treeiter

			treeiter = self.liststore_operations.iter_next (treeiter)

		return None