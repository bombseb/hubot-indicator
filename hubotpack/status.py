# -*- coding: utf-8 -*-

import os
from time import sleep
from threading import Thread
from .vars import *
from .menufunctions import *

class Status(Thread):

	def __init__(self, indicator):
		Thread.__init__(self)
		self.stop = False
		self.indicator = indicator

	def run(self):

		while not self.stop:
			res = os.popen("hubic status").readlines()

			s = res[0].replace ("State: ", "")
			s = s.rstrip ('\n')
			#print ("[{}]".format (s))

			if s in ("Idle"):
				self.indicator.set_icon (ICON_OK)
			elif s == "Paused":
				self.indicator.set_icon (ICON_OK)
				# pauseresume = self.getMenuItem('pauseresume')
				# pauseresume.set_label ("Resume")
				# pauseresume.connect('activate', appMenu.resume)

			elif s == "Busy":
				self.indicator.set_icon (ICON_BUSY)
			elif s in ("Unknown", "NotConnected", "Connecting"):
				self.indicator.set_icon (ICON_ERROR)
			else:
				self.indicator.set_icon (ICON_ERROR)

			self.updateStatus(s)
			sleep(1)

	def arreter(self):
		self.stop = True

	def updateStatus (self, s):
		e = self.getMenuItem ("status")
		e.set_label ("Status : {}".format (s))

	def getMenuItem(self, name):
		menu = self.indicator.get_menu ()
		c = menu.get_children ()

		for e in c:
			if e.get_name() == name: 
				break

		return e

