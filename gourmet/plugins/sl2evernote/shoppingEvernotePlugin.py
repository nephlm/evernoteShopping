import os
import gtk
from gettext import gettext as _

from gourmet.plugin import ShoppingListPlugin
#import gourmet.recipeManager, gourmet.GourmetRecipeManager, time
from gourmet.gglobals import add_icon
from gourmet.prefs import get_prefs

from constants import PREF_NOTESTORE, PREF_DEVTOKEN
import shoppingList

class ShoppingEvernote (ShoppingListPlugin):

    ui_string = '''<ui>
    <menubar name="ShoppingListMenuBar">
      <menu name="File" action="File">
        <placeholder name="ExtraFileStuff">
          <menuitem action="SaveAsEvernote"/>
        </placeholder>
      </menu>
    </menubar>
    <toolbar name="ShoppingListTopToolBar">
      <separator/>
      <toolitem action="SaveAsEvernote"/>
    </toolbar>
    </ui>
    '''
    name = 'shopping_list_evernote'
    label = _('Shopping List Evernote')

    def setup_action_groups (self):
        print('setup_action_groups')
        add_icon(os.path.join(os.path.split(__file__)[0],'images','evernote.png'),
         'evernote',
         _('Evernot Shopping List Saver'))
        self.shoppingListEvernoteActionGroup = gtk.ActionGroup('ShoppingListEvernoteActionGroup')
        self.shoppingListEvernoteActionGroup.add_actions([
            ('File',None,_('File')),
            ('SaveAsEvernote',# name
             # gtk.STOCK_SAVE_AS,# stock
             'evernote', # image
             _('Save List as Evernote'), # text
             _('<Ctrl><Shift>S'), # key-command
             _('Save current shopping list as an Evernote checklist'), # tooltip
             self.save_as_evernote# callback
             ),
            ])
        self.action_groups.append(self.shoppingListEvernoteActionGroup)
        print('appended action group')
        print self.action_groups

    def save_as_evernote(self, *args):
        prefs = get_prefs()
        shopper = self.pluggable.get_shopper(self.pluggable.lst)
        org = shopper.organize(shopper.dic)
        note = ''
        for c,d in org:
            if not c:
                c = _('Unknown')
            note += '<div><h3>' + c.title() + '</h3></div>\n'
            for ingName, amount in d:
                note += "<div><en-todo/>%s (%s)</div>\n" % (ingName, amount)
        #print note
        everNote = shoppingList.ShoppingEverNote(prefs[PREF_DEVTOKEN],
                                prefs[PREF_NOTESTORE], 'Shopping Lists')
        everNote.createShoppingList(note)

        return





