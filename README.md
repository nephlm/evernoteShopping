# evernoteShopping
Evernote shopping list printing for gourmet


3 places where plugins can be located

* .gourmet dir or dir passed in on command line
* "current path"
** os.path.split(os.path.join(os.getcwd(),__file__))[0]
* plugin_base = settings.plugin_base = /usr/share/gourmet

The abc.gourmet-plugin file must go in one of those directories

Module in the .gourmet-plugin file points to a directory in one of the
plugin directories (does not have to be the same one).

In the __init__.py:

``plugins = [plugin1, plugin2]``, probably imported from the local



sudo pip install evernote
