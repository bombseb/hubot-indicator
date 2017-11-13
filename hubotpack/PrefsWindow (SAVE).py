# -*- coding: utf-8 -*-
import os
import gi
import pickle
from .SelectDirs import *
from .LoginWindow import *
from .functions import *
from .vars import *
gi.require_version('Gtk', '3.0')
from gi.repository import Gtk as gtk


class PrefsWindow:
	def __init__(self):
			builder = gtk.Builder()
			builder.add_from_file(os.path.join ('gui', 'prefs.glade'))  # Rentrez évidemment votre fichier, pas le miens!

			self.modifiedList = []

			# self.window 						= builder.get_object('window_prefs')
			# self.notebook_prefs					= builder.get_object('notebook_prefs')

			# # Onglet "Compte"
			# self.label_compte_actuel 			= builder.get_object ('label_compte_actuel')
			# self.label_statut 					= builder.get_object ('label_statut')
			# self.filechooserbutton_emplacement 	= builder.get_object('filechooserbutton_emplacement')
			# self.switch_synchro 				= builder.get_object('switch_synchro')
			# self.button_choix_dossiers  		= builder.get_object('button_choix_dossiers')
			# self.label_emplacement 				= builder.get_object('label_emplacement')
			# self.label_choix_dossiers  			= builder.get_object('label_choix_dossiers')
			# self.frame_synchro 					= builder.get_object('frame_synchro')
			# self.button_valider 				= builder.get_object('button_valider')
			# self.button_annuler 				= builder.get_object('button_annuler')

			# # Onglet "Options avancées"
			# self.switch_proxy					= builder.get_object('switch_proxy')
			# self.label_hote						= builder.get_object('label_hote')
			# self.entry_hote						= builder.get_object('entry_hote')
			# self.label_port						= builder.get_object('label_port')
			# self.entry_port						= builder.get_object('entry_port')
			# self.label_proxy_auth				= builder.get_object('label_proxy_auth')
			# self.switch_proxy_auth				= builder.get_object('switch_proxy_auth')
			# self.label_proxy_user				= builder.get_object('label_proxy_user')
			# self.entry_proxy_user				= builder.get_object('entry_proxy_user')
			# self.label_proxy_passwd				= builder.get_object('label_proxy_passwd')
			# self.entry_proxy_passwd				= builder.get_object('entry_proxy_passwd')

			# # Onglet "Sauvegardes"
			# self.treestore_sauvegardes			= builder.get_object('treestore_sauvegardes')
			# self.treeview_sauvegardes			= builder.get_object('treeview_sauvegardes')


			for o in builder.get_objects():
				if issubclass(type(o), gtk.Buildable):
					name = gtk.Buildable.get_name(o)
					setattr(self, name, o)
			else:
				# print >>sys.stderr, "WARNING: can not get name for '%s'" % o
				print ("WARNING: can not get name for '{}'".format (o))



			self.sauvegardeLoaded = False

			self.excludeList = os.popen("hubic exclude list").readlines ()
			self.excludeList = [x.rstrip ('\n') for x in self.excludeList]	# On supprime le retour chariot à la fin de chaque entrée de la liste

			self.proxyInfoFile = os.path.join(APPDIR, 'proxy')

			# # Le handler
			# handler = {'on_button_login_clicked' 			: self.on_button_login_clicked, 
			#            'on_button_logout_clicked' 			: self.on_button_logout_clicked,
			#            'on_button_choix_dossiers_clicked' 	: self.on_button_choix_dossiers_clicked,
			#            'on_switch_synchro_state_set' 		: self.on_switch_synchro_state_set,
			#            'on_filechooserbutton_emplacement_file_set' : self.on_filechooserbutton_emplacement_file_set,
			#            'on_button_valider_clicked' 			: self.on_button_valider_clicked,
			#            'on_button_annuler_clicked' 			: self.on_button_annuler_clicked,
			#            'on_switch_proxy_state_set'			: self.on_switch_proxy_state_set,
			#            'on_switch_proxy_auth_state_set' 	: self.on_switch_proxy_auth_state_set,
			#            'on_entry_hote_changed'				: self.on_entry_hote_changed,
			#            'on_entry_port_changed' 				: self.on_entry_port_changed,
			#            'on_entry_proxy_user_changed'		: self.on_entry_proxy_user_changed,
			#            'on_entry_proxy_passwd_changed'		: self.on_entry_proxy_passwd_changed,
			#            'on_notebook_prefs_switch_page' : self.on_notebook_prefs_switch_page,
			#            'on_treeview_sauvegardes_row_activated' : self.on_treeview_sauvegardes_row_activated,
			#            'on_button_sauvegarde_modif_clicked' : self.on_button_sauvegarde_modif_clicked}


			builder.connect_signals (self)
			# builder.connect_signals(handler)

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

	def on_button_sauvegarde_modif_clicked (self, button):
		print ("Modifier")

	def on_treeview_sauvegardes_row_activated (self, treeview, path, column):
		self.on_button_sauvegarde_modif_clicked (None)

	def on_notebook_prefs_switch_page (self, notebook, page, page_num):

		if page_num == 2 and not self.sauvegardeLoaded:
			self._set_busy_cursor(True)
			GObject.idle_add(self.afficheSauvegardes)



	def afficheSauvegardes (self):
		iterCetOrdi 	= self.treestore_sauvegardes.append(None, [True, "Cet ordinateur", "", "", "0", False])
		iterAutreOrdi 	= self.treestore_sauvegardes.append(None, [False, "Autres ordinateurs", "", "", "0", False])

		res = os.popen("hubic backup info").readlines()
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
			name = ligne[headerPos['Name'][0]:headerPos['Name'][0] + headerPos['Name'][1]].strip ()
			attached = ligne[headerPos['Attached'][0]:headerPos['Attached'][0] + headerPos['Attached'][1]].strip () == 'Yes'
			localPath = ligne[headerPos['Local path'][0]:headerPos['Local path'][0] + headerPos['Local path'][1]].strip ()
			lastBackup = ligne[headerPos['Last backup'][0]:headerPos['Last backup'][0] + headerPos['Last backup'][1]].strip ()
			size = ligne[headerPos['Size'][0]:headerPos['Size'][0] + headerPos['Size'][1]].strip ()

			if attached:
				self.treestore_sauvegardes.append(iterCetOrdi, [attached, name, localPath, lastBackup, size, True])
			else:
				self.treestore_sauvegardes.append(iterAutreOrdi, [attached, name, localPath, lastBackup, size, True])

		self.treeview_sauvegardes.expand_all ()
		self.sauvegardeLoaded = True
		self._set_busy_cursor (False)


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
			res = os.popen("hubic status").readlines()

			connect = res[3].startswith ('Account: ')

			if connect:
				s = res[3].replace ("Account: ", "")
				s = s.rstrip ('\n')
				print ("[Compte : {}]".format (s))
				self.label_compte_actuel.set_label (s)

				s = res[5].replace ("Usage: ", "")
				s = s.rstrip ('\n')
				print ("[Usage : {}]".format (s))
				self.label_statut.set_label(s)

				s = res[4].replace ("Synchronized directory: ", "")
				s = s.rstrip ('\n')
				if s == '' or not res[4].startswith ('Synchronized directory: ') :
					s = HOMEDIR
					self.switch_synchro.set_state(False)
				else:
					self.switch_synchro.set_state(True)
					print ("[Synchronized directory : {}]".format (s))

				self.filechooserbutton_emplacement.set_filename (s)

			else:
				print ("[Déconnecté]")
				s = 'Déconnecté'
				self.label_compte_actuel.set_label (s)
				self.label_statut.set_label('')
				s = HOMEDIR
				self.filechooserbutton_emplacement.set_filename (s)

			self.frame_synchro.set_sensitive(connect)


	def on_button_login_clicked (self, button):
		LoginWindow(self.afficheInfos)

	def on_button_logout_clicked (self, button):
		os.system ('hubic logout')
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



	# ------ Boutons Valider et Annuler ------
	def on_button_valider_clicked (self, button):

		# Onglet "Compte"
		if self.switch_synchro.get_state ():
			if self.filechooserbutton_emplacement in self.modifiedList:
				cmd = 'hubic syncdir {}'.format (self.filechooserbutton_emplacement.get_filename ())
				print (cmd)
				os.system (cmd)

			if self.excludeList in self.modifiedList:
				cmd = 'hubic exclude clear'
				print (cmd)
				os.system (cmd)
				for path in self.excludeList:
					cmd = 'hubic exclude add {}'.format (path)
					print (cmd)
					os.system (cmd)
		else:
			if self.switch_synchro in self.modifiedList:
				cmd = 'hubic syncdir --none'
				os.system (cmd)


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
				or self.switch_proxy_auth in self.modifiedList:

				proxy = "{} {}".format (proxy_hote, proxy_port)
				user = ""

				if proxy_sw_auth:
					if self.entry_proxy_user in self.modifiedList or self.entry_proxy_passwd in self.modifiedList \
						or self.switch_proxy_auth in self.modifiedList:
						hubicProxyPasswdFile = os.path.join (APPDIR, '.hubicproxypasswd')
						os.system ('echo {} > {}'.format (proxy_passwd, hubicProxyPasswdFile))
						user = "{} {}".format (proxy_user, hubicProxyPasswdFile)

				cmd = 'hubic proxy set {} {}'.format (proxy, user)

		else:
			if self.switch_proxy in self.modifiedList:
				cmd = 'hubic proxy unset'

		print (cmd)

		os.system (cmd)


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

		