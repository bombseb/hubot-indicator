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
import sys
# sys.path.insert(0,"/opt/extras.ubuntu.com/hubot-indicator")
# sys.path.insert(0,"/media/seb/Données/dev/hubot-indicator")

import urllib
import dbus
import urlparse # Python 2.7
import gi
gi.require_version('Nautilus', '3.0')
from gi.repository import Nautilus, GObject
# from hubotpack.HubicDBus import *

# /home/seb/.local/share/nautilus-python/extensions
# /home/seb/.icons/hicolor/24x24/emblems

print ("Hubot -> Python v" + sys.version)


class HubotProvider(GObject.GObject, Nautilus.InfoProvider):
	def update_file_info(self, file): #, update_complete, handle):
		# print ("hubot")
		# uri = urllib.parse.unquote(file.get_uri()).decode('utf8')
		# parsed_uri = urllib.parse.urlparse(uri)
		# if parsed_uri.scheme != 'file': return

		# filepath = os.path.abspath(os.path.join(parsed_uri.netloc, parsed_uri.path))

		uri = urllib.unquote(file.get_uri()).decode('utf8')
		parsed_uri = urlparse.urlparse(uri)
		if parsed_uri.scheme != 'file': return
		filepath = os.path.abspath(os.path.join(parsed_uri.netloc, parsed_uri.path))

		# hubicAccount = HubicAccount ()

		# ret = [u'', True, True]


		# format_value = dbus.Array([dbus.Byte(0x14),  # format: 32 bit float
  #                              dbus.Byte(0x00),  # exponent
  #                              dbus.Byte(0xAD),  # LSB of unit (%)
  #                              dbus.Byte(0x27),  # MSB of unit (%)
  #                              dbus.Byte(0x01),  # namespace
  #                              dbus.Byte(0x00),  # LSB of description
  #                              dbus.Byte(0x00)])  # MSB of description


		# ret = dbus.Array([dbus.String(""), dbus.Boolean(""), dbus.Boolean("")])


		status = ""
		isPublished = False
		canBePublished = False

		session_bus = dbus.SessionBus()
		hubic_account_obj = session_bus.get_object('com.hubiC', '/com/hubic/Account')
		hubic_account_iface = dbus.Interface(hubic_account_obj, 'com.hubic.account')
		[status, isPublished, canBePublished] = hubic_account_iface.GetItemStatus(filepath)

		# ret = hubicAccount.getItemStatus (filepath)
		
		# print (status + "\t" + filepath)

		# status = "Synchronized"

		if status == "Synchronized":
			file.add_emblem("hubot-synchronized")
		elif status == "Unsynchronized":
			file.add_emblem("hubot-syncing")
		else:
			return


	# com.hubic.account
	# # GetItemStatus (IN  s     absolutePath, OUT (sbb) ret);

	# Status (string)
	# The synchronization status. It can be Synchronized (file is ok), Unsynchronized (the file is either downloading or uploading), NoStatus (the file is filtered out or outside of synchronized directory) or else Error when an unexpected exception happen.

	# IsPublished (bool)
	# Whether the item is published or not.

	# CanBePublished (bool)
	# Whether the item could be published. It this is false, trying to Publish() the item will certainly fail.
