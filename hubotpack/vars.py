# -*- coding: utf-8 -*-
import os
from pathlib import Path

APPINDICATOR_ID = 'hubot-indicator'

ICON_OK         = os.path.abspath(os.path.join ('icons','ok.svg'))
ICON_ERROR		= os.path.abspath(os.path.join ('icons','error.svg'))
ICON_DOWNLOAD   = os.path.abspath(os.path.join ('icons','download.svg'))
ICON_UPLOAD     = os.path.abspath(os.path.join ('icons','upload.svg'))
ICON_BUSY       = os.path.abspath(os.path.join ('icons','busy.svg'))

HOMEDIR = str(Path.home())
APPDIR = os.path.join (HOMEDIR, '.config', 'hubot-indicator')
if not os.path.exists (APPDIR): os.mkdir (APPDIR)


