# -*- coding: utf-8 -*-
import os
import gi
import pickle
from .SelectDirs import *
from .LoginWindow import *
from .Sauvegarde import *
from .functions import *
from .HubicBackup import *
# from .BackupInProgressWatcher import *
from .vars import *
gi.require_version('Gtk', '3.0')
from gi.repository import Gtk as gtk
import dbus

class PrefsWindow:
	def __init__(self):
		builder = gtk.Builder()
		builder.add_from_file(os.path.join ('gui', 'prefs.glade'))  # Rentrez évidemment votre fichier, pas le miens!

		self.modifiedList = []

		for o in builder.get_objects():
			if issubclass(type(o), gtk.Buildable):
				name = gtk.Buildable.get_name(o)
				setattr(self, name, o)

		self.sauvegardeLoaded = False

		self.hubicAccountObj = SESSION_BUS.get_object(BUSNAME, '/com/hubic/Account')
		self.hubicSettingsObj = SESSION_BUS.get_object(BUSNAME, '/com/hubic/Settings')
		self.excludeList = self.hubicAccountObj.Get('com.hubic.account', 'ExcludedFolders')
		self.proxyInfoFile = os.path.join(APPDIR, 'proxy')
		self.iterCetOrdi 	= self.treestore_sauvegardes.append(None, [True, "Cet ordinateur", "", "", "0", False, False])
		self.iterAutreOrdi 	= self.treestore_sauvegardes.append(None, [False, "Autres ordinateurs", "", "", "0", False, False])
		# self.backupWatcher = BackupInProgressWatcher (self.treestore_sauvegardes)

		builder.connect_signals (self)

		# Chargement des infos de connexion au proxy :
		try:
			with open(self.proxyInfoFile, 'rb') as fichier:
				mon_depickler = pickle.Unpickler(fichier)
				self.switch_proxy.set_state (mon_depickler.load())
				self.entry_hote.set_text (mon_depickler.load())
				self.entry_port.set_text (mon_depickler.load())
				self.switch_proxy_auth.set_state (mon_depickler.load())
				self.entry_proxy_user.set_text (mon_depickler.load())
				self.entry_proxy_passwd.set_text (mon_depickler.load())
		except FileNotFoundError:
			pass

		self.modifiedList.clear ()
		self.afficheInfos()

		self.window_prefs.show_all()
		#self.window.present ()
		#self.window.set_keep_above (True)



	def _set_busy_cursor(self, busy):
		cursor = None

		if busy:
			cursor = gdk.Cursor(gdk.CursorType.WATCH)
		else:
			cursor = gdk.Cursor(gdk.CursorType.LEFT_PTR)

		gdk_window = self.window_prefs.get_window()
		gdk_window.set_cursor(cursor)

		
	# ------ Onglet "Compte" ------
	def afficheInfos (self):
		account = self.hubicAccountObj.Get('com.hubic.account', 'Account')

		connect = account != ''

		if connect:
			self.label_compte_actuel.set_label (account)

			usedBytes = str (convert_size (self.hubicAccountObj.Get('com.hubic.account', 'UsedBytes')))
			totalBytes = str (convert_size (self.hubicAccountObj.Get('com.hubic.account', 'TotalBytes')))
			usage = "{} sur {}".format (usedBytes, totalBytes)
			self.label_statut.set_label(usage)

			synchronizedDir = self.hubicAccountObj.Get('com.hubic.account', 'SynchronizedDir')

			if synchronizedDir == '':
				synchronizedDir = HOMEDIR
				self.switch_synchro.set_state(False)
			else:
				self.switch_synchro.set_state(True)

			self.filechooserbutton_emplacement.set_filename (synchronizedDir)

		else:
			s = 'Déconnecté'
			self.label_compte_actuel.set_label (s)
			self.label_statut.set_label('')
			s = HOMEDIR
			self.filechooserbutton_emplacement.set_filename (s)

		self.frame_synchro.set_sensitive(connect)


	def on_button_login_clicked (self, button):
		LoginWindow(self.afficheInfos)

	def on_button_logout_clicked (self, button):
		self.hubicAccountObj.Logout (dbus_interface='com.hubic.account')
		self.afficheInfos ()

		self.switch_synchro.set_state (False)

	def on_filechooserbutton_emplacement_file_set (self, file_chooser):
		self.modifiedList.append (self.filechooserbutton_emplacement)
		self.excludeList.clear ()
		self.modifiedList.append (self.excludeList)

	def on_button_choix_dossiers_clicked(self, emplacement):
		rootDir = emplacement.get_filename ()
		if rootDir == '': return
		SelectDirs (self, rootDir)
		
	def on_switch_synchro_state_set(self, switch, state):
		self.filechooserbutton_emplacement.set_sensitive (state)
		self.button_choix_dossiers.set_sensitive (state)
		self.label_choix_dossiers.set_sensitive(state)
		self.label_emplacement.set_sensitive(state)
		self.modifiedList.append (self.switch_synchro)


	# ------ Onglet Options avancées ------
	def on_switch_proxy_state_set(self, switch, state):

		self.label_hote.set_sensitive (state)
		self.entry_hote.set_sensitive (state)
		self.label_port.set_sensitive (state)
		self.entry_port.set_sensitive (state)
		self.label_proxy_auth.set_sensitive (state)
		self.switch_proxy_auth.set_sensitive (state)

		if not state: self.switch_proxy_auth.set_state(False)

		self.modifiedList.append (self.switch_proxy)

	def on_switch_proxy_auth_state_set(self, switch, state):
		self.label_proxy_user.set_sensitive (state)
		self.entry_proxy_user.set_sensitive (state)
		self.label_proxy_passwd.set_sensitive (state)
		self.entry_proxy_passwd.set_sensitive (state)

		self.modifiedList.append (self.switch_proxy_auth)


	def on_entry_hote_changed(self, editable):
		self.modifiedList.append (self.entry_hote)

	def on_entry_port_changed(self, editable):
		text = self.entry_port.get_text().strip()
		self.entry_port.set_text(''.join([i for i in text if i in '0123456789']))
		self.modifiedList.append (self.entry_port)

	def on_entry_proxy_user_changed(self, editable):
		self.modifiedList.append (self.entry_proxy_user)

	def on_entry_proxy_passwd_changed(self, editable):
		self.modifiedList.append (self.entry_proxy_passwd)


	# ------ Onglet Sauvegardes ------
	def on_notebook_prefs_switch_page (self, notebook, page, page_num):
		if page_num == 2 and not self.sauvegardeLoaded:
			self._set_busy_cursor(True)
			GObject.idle_add(self.afficheSauvegardes)
			self.sauvegardeLoaded = True

	def afficheSauvegardes (self):	

		res = os.popen("hubic backup info").readlines()
		if len (res) == 0: return
		res = [x.rstrip ('\n') for x in res]

		header = ['Name','Attached','Local path','Last backup','Size']
		headerPos = {}
		pos = 0
		for e in header:
			length = res[0].find (e) + len (e) - pos
			headerPos[e] = (pos, length)
			pos += length

		test = []
		for i, ligne in enumerate (res):
			if i == 0 : continue
			name = ligne[headerPos['Name'][0]:headerPos['Name'][0] + headerPos['Name'][1]].strip ().replace (' ', '_')
			attached = ligne[headerPos['Attached'][0]:headerPos['Attached'][0] + headerPos['Attached'][1]].strip () == 'Yes'
			localPath = ligne[headerPos['Local path'][0]:headerPos['Local path'][0] + headerPos['Local path'][1]].strip ()
			lastBackup = ligne[headerPos['Last backup'][0]:headerPos['Last backup'][0] + headerPos['Last backup'][1]].strip ()
			size = ligne[headerPos['Size'][0]:headerPos['Size'][0] + headerPos['Size'][1]].strip ()

			if attached:
				self.treestore_sauvegardes.append(self.iterCetOrdi, [attached, name, localPath, lastBackup, size, True, False])
			else:
				self.treestore_sauvegardes.append(self.iterAutreOrdi, [attached, name, localPath, lastBackup, size, True, False])

		self.treeview_sauvegardes.expand_all ()
		# self.backupWatcher.start ()

		self._set_busy_cursor (False)

	def on_treeview_sauvegardes_row_activated (self, treeview, path, column):
		self.on_button_sauvegarde_modif_clicked (None)

	def on_treeview_sauvegardes_cursor_changed(self, treeview):
		treeselection = self.treeview_sauvegardes.get_selection()
		(model, iterSelection) = treeselection.get_selected()

		child = self.treestore_sauvegardes.get_value (iterSelection, 5)
		attached = self.treestore_sauvegardes.get_value (iterSelection, 0)

		self.button_sauvegarde_maj.set_sensitive (child and attached)
		self.button_sauvegarde_attacher.set_sensitive (child and not attached)
		self.button_sauvegarde_supprimer.set_sensitive (child)
		self.button_sauvegarde_modif.set_sensitive (child)
		self.button_sauvegarde_download.set_sensitive (child)


	def on_button_sauvegarde_creer_clicked (self, button):
		Sauvegarde (self)



	def on_button_sauvegarde_supprimer_clicked (self, button):
		response = self.dialog_sauvegarde_suppr.run()
		self.dialog_sauvegarde_suppr.hide()

		if response == 1:
			treeselection = self.treeview_sauvegardes.get_selection()
			(model, iterSelection) = treeselection.get_selected()
			name = self.treestore_sauvegardes.get_value (iterSelection, 1)
			self.treestore_sauvegardes.remove (iterSelection)
			b = HubicBackup (name)
			b.delete ()

	def on_button_sauvegarde_modif_clicked (self, button):
		treeselection = self.treeview_sauvegardes.get_selection()
		(model, iterSelection) = treeselection.get_selected()

		child = self.treestore_sauvegardes.get_value (iterSelection, 5)
		if child:
			Sauvegarde (self, iterSelection)

	def on_button_sauvegarde_maj_clicked(self, button):
		b = HubicBackup (self.getBackupNameFromSelection ())
		b.backupNow ()

	def on_button_sauvegarde_downattach_clicked(self, button):
		response = self.filechooserdialog_selection_repertoire.run()
		self.filechooserdialog_selection_repertoire.hide()

		if response != 1: return

		path = self.filechooserdialog_selection_repertoire.get_filename ()
		if os.listdir(path):
			messageBox (self.window_prefs, "Le répertoire de destination doit être vide !", messageType=gtk.MessageType.ERROR)
			return

		b = HubicBackup (self.getBackupNameFromSelection ())
		if button == self.button_sauvegarde_download:
			b.downloadInto (path)
		elif button == self.button_sauvegarde_attacher:
			b.attachToThisComputer (path)


	def getBackupNameFromSelection (self):
		treeselection = self.treeview_sauvegardes.get_selection()
		(model, iterSelection) = treeselection.get_selected()
		name = self.treestore_sauvegardes.get_value (iterSelection, 1)

		return name


	# ------ Boutons Valider et Annuler ------
	def on_button_valider_clicked (self, button):

		cmd = ''

		# Onglet "Compte"
		if self.switch_synchro.get_state ():
			if self.filechooserbutton_emplacement in self.modifiedList:
				synchroPath = self.filechooserbutton_emplacement.get_filename ()
				# self.hubicAccountIFace2.Set('com.hubic.account', 'SynchronizedDir', synchroPath)
				self.hubicAccountObj.Set ('com.hubic.account', 'SynchronizedDir', synchroPath, dbus_interface='org.freedesktop.DBus.Properties')

			if self.excludeList in self.modifiedList:
				self.hubicAccountObj.Set ('com.hubic.account', 'ExcludedFolders', self.excludeList, dbus_interface='org.freedesktop.DBus.Properties')
		else:
			if self.switch_synchro in self.modifiedList:
				self.hubicAccountObj.Set ('com.hubic.account', 'SynchronizedDir', '', dbus_interface='org.freedesktop.DBus.Properties')


		# Onglet "Options avancées"
		proxy_sw = self.switch_proxy.get_state ()
		proxy_hote = self.entry_hote.get_text ()
		proxy_port = self.entry_port.get_text ()
		proxy_sw_auth = self.switch_proxy_auth.get_state ()
		proxy_user = self.entry_proxy_user.get_text ()
		proxy_passwd = self.entry_proxy_passwd.get_text ()


		if proxy_sw:
			if proxy_hote == "":
				self.notebook_prefs.set_current_page (1)
				messageBox (self.window_prefs, "Veuillez saisir le nom d'hôte pour le proxy")
				return

			if proxy_port == "":
				self.notebook_prefs.set_current_page (1)
				messageBox (self.window_prefs, "Veuillez saisir le port pour le proxy")
				return

			if proxy_sw_auth:
				if proxy_user == "":
					self.notebook_prefs.set_current_page (1)
					messageBox (self.window_prefs, "Veuillez saisir le nom d'utilisateur pour la connexion par le proxy")
					return

				if proxy_passwd == "":
					self.notebook_prefs.set_current_page (1)
					messageBox (self.window_prefs, "Veuillez saisir le mot de passe pour la connexion par le proxy")
					return

			if self.entry_hote in self.modifiedList or self.entry_port in self.modifiedList or \
				self.entry_proxy_user in self.modifiedList or self.entry_proxy_passwd in self.modifiedList \
				or self.switch_proxy_auth in self.modifiedList or self.switch_proxy in self.modifiedList:

				if proxy_sw_auth:
					if self.entry_proxy_user in self.modifiedList or self.entry_proxy_passwd in self.modifiedList \
						or self.switch_proxy_auth in self.modifiedList:
						self.hubicSettingsObj.SetAuthenticatedProxy (proxy_hote, int (proxy_port), proxy_user, proxy_passwd, dbus_interface='com.hubic.settings')
				else:
					self.hubicSettingsObj.SetProxy (proxy_hote, int (proxy_port), dbus_interface='com.hubic.settings')

		else:
			if self.switch_proxy in self.modifiedList:
				self.hubicSettingsObj.UnsetProxy (dbus_interface='com.hubic.settings')

		# Sauvegarde des objets dans un fichier de données :
		with open(self.proxyInfoFile, 'wb') as fichier:
			p = pickle.Pickler(fichier)
			p.dump(proxy_sw)
			p.dump(proxy_hote)
			p.dump(proxy_port)
			p.dump(proxy_sw_auth)
			p.dump(proxy_user)
			p.dump(proxy_passwd)

		self.window_prefs.close ()


	def on_button_annuler_clicked (self, button):
		self.window_prefs.close ()
