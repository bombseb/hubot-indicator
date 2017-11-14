#! /usr/bin/python3
# -*- coding: utf-8 -*-
import signal
import os
import gi
from hubotpack.vars import *
from hubotpack.AppMenu import *

gi.require_version('Gtk', '3.0')
gi.require_version('AppIndicator3', '0.1')
from gi.repository import AppIndicator3 as appindicator


def main():
    signal.signal(signal.SIGINT, signal.SIG_DFL)
    #indicator = appindicator.Indicator.new(APPINDICATOR_ID, 'whatever', appindicator.IndicatorCategory.SYSTEM_SERVICES)
    #indicator = appindicator.Indicator.new(APPINDICATOR_ID, gtk.STOCK_INFO, appindicator.IndicatorCategory.SYSTEM_SERVICES)
    indicator = appindicator.Indicator.new(APPINDICATOR_ID, ICON_ERROR, appindicator.IndicatorCategory.SYSTEM_SERVICES)	
    indicator.set_status(appindicator.IndicatorStatus.ACTIVE)
    indicator.set_menu(AppMenu (indicator))

    gtk.main()


if __name__ == "__main__":
    main()
