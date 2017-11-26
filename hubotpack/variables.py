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
