# evernoteShopping

Evernote shopping list printing for gourmet.  This is a plugin for
the gourmet recipe manager (http://thinkle.github.io/gourmet/).
Gourment comes natively with a shopping list generator however your
only choices are to print or save those lists.  This plugin allows
the user to send the shopping lists to their evernote account
and be accessible from their phones.

To use the plugin you will need an evernote account
(https://evernote.com/) and a developer token
(https://www.evernote.com/api/DeveloperToken.action).

Developer tokens are some what mis-named, they are the recommended
keys for accessing your evernote account from a desktop app such
as Gourmet.  Evernote's OAuth implementation doesn't support an
out of band authentication nor a username/password authentication
making the developer token the choice by default.

# Requirements

At present installation is a manual process.  If someone besides me starts using this I'll look into writing a setup.py script.

Gourmet must be installed and able to be run.  In addition to
Gourmet the Evernote API must be installed.

```sh
REPO=<directory where this file is located>
sudo pip install -r $REPO/requirements.txt
```

or

```sh
sudo pip install evernote
```

Either should install all missing requirements.

# Installation

## Find a plugin directory

There are three plugin directories on any installation.

* ``~/.gourmet/plugins`` dir or dir passed in on command line
  * Only installs for the local user.
* "current path"
  * This is relative to the installed Gourmet libraries
  * Probably something like ``/usr/lib/python2.7/dist-packages/gourmet/plugins``
    * ``os.path.split(os.path.join(os.getcwd(),__file__))[0]`` run
    from ``plugin_loader.py``
* plugin_base
  * Usually something like ``/usr/share/gourmet``

I don't know what the windows equivalent of these would be.

## Copy files

Assuming you are doing a per user install you'd do something like
the following.  For system wide install you'd need to change the
copy destination to one of the other plugin dirs.

```sh
PLUGIN_DIR=~/.gourmet/plugins
REPO=<directory where this file is located>
cp $REPO/gourmet/plugins/*.gourmet-plugin $GOURMET_DIR
cp -r $REPO/gourmet/plugins/sl2Evernote $GOURMET_DIR/
```


# Random Notes that Need a new home

The abc.gourmet-plugin file must go in one of those directories

Module in the .gourmet-plugin file points to a directory in one of the
plugin directories (does not have to be the same one).

In the __init__.py:

``plugins = [plugin1, plugin2]``, probably imported from the local

