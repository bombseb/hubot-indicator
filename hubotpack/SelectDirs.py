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
gi.require_version('Gtk', '3.0')
from gi.repository import Gtk as gtk



class SelectDirs:
	def __init__(self, parent, rootDir):
			builder = gtk.Builder()
			builder.add_from_file(os.path.join (APPDIR, 'gui', 'selectDirs.glade'))

			self.window = builder.get_object('window_selectDirs')
			self.treeStore = builder.get_object('treestore_dirs')

			self.rootDir = rootDir

			# Le handler
			handler = {'on_cellrenderertoggle_toggled' : self.on_cellrenderertoggle_toggled,
						'on_button_ok_clicked' : self.on_button_ok_clicked,
						'on_button_annuler_clicked' : self.on_button_annuler_clicked}
			builder.connect_signals(handler)

			# Affiche tous les sous répertoire du répertoire racine à synchroniser
			self.parent = parent
			self.excludeList = parent.excludeList
			self.afficheDirs(None, rootDir)

			# On développe le treeview
			self.treeview = builder.get_object('treeview_select')
			self.treeview.expand_all ()
			self.window.show_all()

	def on_cellrenderertoggle_toggled(self, widget, path):
		self.treeStore[path][0] = not self.treeStore[path][0]

	def afficheDirs(self, rootIter, rootDir):

		#print (rootDir)

		read_write = os.access (rootDir, os.X_OK)
		if not read_write:
			return

		try:
			for e in os.listdir(rootDir):
				path = os.path.join (rootDir,e)
				if os.path.isdir (path):
					select = path not in self.excludeList
					dirIter = self.treeStore.append(rootIter, [select, e])
					self.afficheDirs(dirIter, path)
		except PermissionError:
			return

	def getExcludeDirs(self, currentIter, rep):

		while currentIter:
			checked = self.treeStore.get_value (currentIter, 0)
			path = os.path.join (rep, self.treeStore.get_value (currentIter, 1))

			if not checked: 
				self.excludeList.append(path)

			childIter = self.treeStore.iter_children(currentIter)
			if childIter:
				self.getExcludeDirs (childIter, path )

			currentIter = self.treeStore.iter_next(currentIter)

	def on_button_ok_clicked(self, button):

		self.excludeList.clear ()

		firstIter = self.treeStore.get_iter_first()
		self.getExcludeDirs (firstIter, self.rootDir)

		self.window.close ()
		self.parent.modifiedList.append (self.excludeList)

	def on_button_annuler_clicked(self, button):
		self.window.close ()
