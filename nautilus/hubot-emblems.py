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
import urllib
import dbus
import urlparse # Python 2.7
import gi
gi.require_version('Nautilus', '3.0')
from gi.repository import Nautilus, GObject

print ("Hubot -> Python v" + sys.version)


class HubotProvider(GObject.GObject, Nautilus.InfoProvider):
	def update_file_info(self, file): #, update_complete, handle):
		uri = urllib.unquote(file.get_uri()).decode('utf8')
		parsed_uri = urlparse.urlparse(uri)
		if parsed_uri.scheme != 'file': return
		filepath = os.path.abspath(os.path.join(parsed_uri.netloc, parsed_uri.path))

		# status = ""
		# isPublished = False
		# canBePublished = False

		session_bus = dbus.SessionBus()
		hubic_account_obj = session_bus.get_object('com.hubiC', '/com/hubic/Account')
		hubic_account_iface = dbus.Interface(hubic_account_obj, 'com.hubic.account')
		[status, isPublished, canBePublished] = hubic_account_iface.GetItemStatus(filepath)

		if status == "Synchronized":
			file.add_emblem("hubot-synchronized")
		elif status == "Unsynchronized":
			file.add_emblem("hubot-syncing")
		else:
			return
