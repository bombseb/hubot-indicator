# -*- coding: utf-8 -*-
import os
import gi
import math
from .vars import *
from .functions import *
gi.require_version('Gtk', '3.0')
from gi.repository import Gtk as gtk, GObject, GdkPixbuf

class RunningOperations:
	def __init__(self):
		builder = gtk.Builder()
		builder.add_from_file(os.path.join ('gui', 'runningoperations.glade'))

		for o in builder.get_objects():
			if issubclass(type(o), gtk.Buildable):
				name = gtk.Buildable.get_name(o)
				setattr(self, name, o)

		builder.connect_signals (self)

		self.iconDown	= GdkPixbuf.Pixbuf.new_from_file_at_size(ICON_DOWNLOAD, -1, 24)
		self.iconUp		= GdkPixbuf.Pixbuf.new_from_file_at_size(ICON_UPLOAD, -1, 24)

		self.window_running_operations.show_all()

		self.timeout_id = GObject.timeout_add(100, self.raffraichir)

	def raffraichir(self):
		result = hubicAccount.getProperty ('RunningOperations')

		if len (result) > 0:
			# Mise à jour des lignes
			for operation in result:
				bytesDone = operation[4]
				totalBytes = operation[5]
				if totalBytes > 0:
					pourcentage = (bytesDone / totalBytes) * 100
				else:
					pourcentage = 0

				pourcentage = math.floor(pourcentage)
				iterLigne = self.getIterFromID(operation[0])

				progress_text = "{}% ({}/{})".format(pourcentage, convert_size(bytesDone), convert_size(totalBytes))

				if not iterLigne:
					if operation[3].lower().strip () == "download":
						icon = self.iconDown
					elif operation[3].lower().strip () == "upload":
						icon = self.iconUp
					else:
						icon = None

					self.liststore_operations.append ([operation[0], operation[1], operation[2], icon, bytesDone, totalBytes, pourcentage, progress_text])
				elif totalBytes > 0: 
						self.liststore_operations.set_value(iterLigne, 5, totalBytes)
						self.liststore_operations.set_value(iterLigne, 6, pourcentage)
						self.liststore_operations.set_value(iterLigne, 7, progress_text)


		# Supression des lignes
		for ligne in reversed (self.liststore_operations):
			idOp = None
			for operation in result:
				idOp = operation[0]
				if idOp == ligne[0]: break

			if idOp != ligne[0]:
				treeIter = self.getIterFromID (ligne[0])
				self.liststore_operations.remove (treeIter)


		return True

	def getIterFromID (self, idOp):
		treeiter = self.liststore_operations.get_iter_first()
		while treeiter:
			tmpID = self.liststore_operations.get_value (treeiter, 0)
			if tmpID == idOp:
				return treeiter

			treeiter = self.liststore_operations.iter_next (treeiter)

		return None