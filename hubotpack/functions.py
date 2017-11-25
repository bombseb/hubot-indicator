# -*- coding: utf-8 -*-
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