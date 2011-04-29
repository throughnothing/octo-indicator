# Octo-Indicator
`octo-indicator` is an appindicator that shows your github activity feed in the menubar of ubuntu.  This is mostly just a test app for me to learn how appindicators work.

# Install

Currently requires `feedparser`, `github2`, `pygtk` python modules.  If you have all the modules, just modify octo-indicator's GH\_USER and GH\_TOKEN values near the top of the file and then run it.

It currently reads your github username/token from `~/.octoindicatorrc`

    [github]
    user=throughnothing
    token=<TOKEN-HERE>

Once you have all of the requirements, you can install with
    
    python setup.py install

# TODO

* Use config file/dconf (preferably dconf)
* Pull gravatar icons
* Add libnotify support
