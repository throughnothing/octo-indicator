# -*- Mode: Python; coding: utf-8; indent-tabs-mode: nil; tab-width: 4 -*-
### BEGIN LICENSE
# This file is in the public domain
### END LICENSE

import gettext
from gettext import gettext as _
gettext.textdomain('octoindicator')

import appindicator
import gtk
import logging
logger = logging.getLogger('octoindicator')

import ConfigParser
import feedparser
import github2.client as gh
import os
import webbrowser

from octoindicator_lib import Window
from octoindicator.AboutOctoindicatorDialog import AboutOctoindicatorDialog
from octoindicator.PreferencesOctoindicatorDialog import PreferencesOctoindicatorDialog

GH_FEED_UPDATE_INTERVAL=1000*60*10 # 10 minutes
GH_FEED_UPDATE_INTERVAL=120000 # 15 seconds
GH_FEED_ITEMS=25

# See octoindicator_lib.Window.py for more details about how this class works
class OctoindicatorWindow(object):
    __gtype_name__ = "OctoindicatorWindow"
    
    def __init__(self): # pylint: disable=E1002
        """Set up the main window"""

        self.AboutDialog = AboutOctoindicatorDialog
        self.PreferencesDialog = PreferencesOctoindicatorDialog

        # Code for other initialization actions should be added here.

        self.config = ConfigParser.ConfigParser()
        self.config.read(os.path.join(os.path.expanduser('~'),'.octoindicatorrc'))
        self.gh_user=self.config.get('github','user')
        self.gh_token=self.config.get('github','token')
        self.latest_entry_id = ''

        if not self.gh_user or not self.gh_token:
            raise Exception('User or Token could not be found in ~/.octoindicatorrc') 
        self.gh_feed_url = ("https://github.com/%s.private.atom?token=%s" % 
            (self.gh_user, self.gh_token))
    
        appdir = '/usr/local/share/octoindicator/media/'
        self.ind = appindicator.Indicator ("octo-indicator",
                                  os.path.join(appdir,"octocat.png"),
                                  appindicator.CATEGORY_COMMUNICATIONS)
        self.ind.set_status (appindicator.STATUS_ACTIVE)
        self.ind.set_attention_icon (os.path.join(appdir,"octocat-active.png"))

        # create a menu
        self.menu = gtk.Menu()

        refresh_item = gtk.MenuItem('_Refresh')
        self.menu.append(refresh_item)
        refresh_item.connect("activate", self.refresh_click)
        refresh_item.show()

        clear_item = gtk.MenuItem('_Mark all as seen')
        self.menu.append(clear_item)
        clear_item.connect("activate", self.mark_read_click)
        clear_item.show()
        
        #Separator
        separator_item = gtk.SeparatorMenuItem()
        self.menu.append(separator_item)

        separator_item.show()

        self.ind.set_menu(self.menu)

        # Get initial feed
        gtk.timeout_add(100,self.update_feed)


    def update_feed(self):
        gh_feed = feedparser.parse(self.gh_feed_url)

        if gh_feed['entries'][0]['id'] == self.latest_entry_id:
            print "nothing to update"
            gtk.timeout_add(GH_FEED_UPDATE_INTERVAL, self.update_feed)
            return # nothing to update

        # Clear old entries
        cur_menu_items = self.menu.get_children()
        for i in range(3,len(cur_menu_items)):
            self.menu.remove(cur_menu_items[i])

        self.latest_entry_id = gh_feed['entries'][0]['id']
        self.ind.set_status (appindicator.STATUS_ATTENTION)

        # Repopulate menu items
        i = 0
        for entry in gh_feed['entries']:
            i = i + 1
            if i > GH_FEED_ITEMS:
                break

            t = entry['title_detail']['value']
            menu_item = gtk.MenuItem(t)
            self.menu.append(menu_item)
            menu_item.connect("activate", self.feeditem_click,entry)
            menu_item.show()


        gtk.timeout_add(GH_FEED_UPDATE_INTERVAL, self.update_feed)

    def feeditem_click(self, w, entry):
        self.ind.set_status (appindicator.STATUS_ACTIVE)
        webbrowser.open(entry['links'][0]['href'])

    def mark_read_click(self, w):
        self.ind.set_status (appindicator.STATUS_ACTIVE)

    def refresh_click(self, w):
        self.update_feed()

