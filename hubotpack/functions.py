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

import math
import gi
gi.require_version('Gtk', '3.0')
from gi.repository import Gtk as gtk

def messageBox(parent, text, messageType=gtk.MessageType.WARNING):
  #gtk.MessageType :
  #'WARNING', ERROR', 'INFO', 'OTHER', 'QUESTION', 'WARNING'
  md = gtk.MessageDialog(parent=parent, flags=0, type=messageType, buttons=gtk.ButtonsType.OK, message_format=text)

  md.run()
  md.destroy()

def convert_size(size):
  if (size <= 0): return '0 Octets'

  size_name = ("Octets", "Ko", "Mo", "Go", "To", "Po", "Eo", "Zo", "Yo")
  i = int(math.floor(math.log(size,1024)))
  p = math.pow(1024,i)
  s = round(size/p,2)
  return "{} {}".format(s, size_name[i])