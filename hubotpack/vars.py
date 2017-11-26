# -*- coding: utf-8 -*-
import os
from pathlib import Path
from .HubicDBus import *

APPINDICATOR_ID = 'hubot-indicator'

ICON_IDLE         	= os.path.abspath(os.path.join ('icons','idle.svg'))
ICON_BUSY       	= os.path.abspath(os.path.join ('icons','busy.svg'))
ICON_PAUSE      	= os.path.abspath(os.path.join ('icons','pause.svg'))
ICON_NOTCONNECTED	= os.path.abspath(os.path.join ('icons','notconnected.svg'))
ICON_ERROR			= os.path.abspath(os.path.join ('icons','error.svg'))
ICON_DOWNLOAD   	= os.path.abspath(os.path.join ('icons','download.svg'))
ICON_UPLOAD     	= os.path.abspath(os.path.join ('icons','upload.svg'))

HOMEDIR = str(Path.home())
APPDIR = os.path.join (HOMEDIR, '.config', 'hubot-indicator')
if not os.path.exists (APPDIR): os.mkdir (APPDIR)

hubicAccount = HubicAccount ()
hubicGeneral = HubicGeneral ()
