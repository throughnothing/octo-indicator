# -*- Mode: Python; coding: utf-8; indent-tabs-mode: nil; tab-width: 4 -*-
### BEGIN LICENSE
# This file is in the public domain
### END LICENSE

import optparse

import gettext
from gettext import gettext as _
gettext.textdomain('octoindicator')

import gtk

from octoindicator import OctoindicatorWindow

from octoindicator_lib import set_up_logging, preferences, get_version

def parse_options():
    """Support for command line options"""
    parser = optparse.OptionParser(version="%%prog %s" % get_version())
    parser.add_option(
        "-v", "--verbose", action="count", dest="verbose",
        help=_("Show debug messages (-vv debugs octoindicator_lib also)"))
    (options, args) = parser.parse_args()

    set_up_logging(options)

def main():
    'constructor for your class instances'
    parse_options()

    # preferences
    # set some values for our first session
    # TODO: replace defaults with your own values
    default_preferences = {
    'example_entry': 'I remember stuff',
    }
    preferences.update(default_preferences)
    # user's stored preferences are used for 2nd and subsequent sessions
    preferences.db_connect()
    preferences.load()

    # Run the application.    
    window = OctoindicatorWindow.OctoindicatorWindow()
    gtk.main()
    
    preferences.save()
