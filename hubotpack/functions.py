# -*- coding: utf-8 -*-
import gi
gi.require_version('Gtk', '3.0')
from gi.repository import Gtk as gtk

def messageBox(parent, text, messageType=gtk.MessageType.WARNING):
    #gtk.MessageType :
    #'WARNING', ERROR', 'INFO', 'OTHER', 'QUESTION', 'WARNING'


    md = gtk.MessageDialog(parent=parent, flags=0, type=messageType, buttons=gtk.ButtonsType.OK, message_format=text)

    md.run()
    md.destroy()
