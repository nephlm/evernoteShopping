"""
Plugin implementing the ''print to evernote'' function on the
shopping list page.
"""

import os
from gi.repository import Gtk, GdkPixbuf
from gettext import gettext as _

from gourmand.plugin import ShoppingListPlugin

# import gourmet.recipeManager, gourmet.GourmetRecipeManager, time
from gourmand.gglobals import add_icon
from gourmand.prefs import Prefs

from evernote.edam.error.ttypes import EDAMUserException

from sl2evernote.constants import PREF_NOTEBOOK, PREF_DEVTOKEN, DEFAULT_NOTEBOOK
import sl2evernote.shoppingList as shoppingList


class ShoppingEvernote(ShoppingListPlugin):
    """
    Plugin to give the user the option to save shopping lists to
    evernote. Requires a dev key be setup in prefs.
    """

    # Sets up save as evernote menu item and icon
    ui_string = """<ui>
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
    """
    ui = ui_string

    # plugin metadata
    name = "shopping_list_evernote"
    label = _("Shopping List Evernote")

    def setup_action_groups(self):
        """
        Hook up the ui elements created by ui_string to actions.
        Called by plugin manager.
        """
        add_icon(
            GdkPixbuf.Pixbuf.new_from_file(
                os.path.join(os.path.split(__file__)[0], "images", "evernote.png")
            ),
            "evernote",
            _("Evernote Shopping List Saver"),
        )
        shoppingListEvernoteActionGroup = Gtk.ActionGroup(
            "ShoppingListEvernoteActionGroup"
        )
        shoppingListEvernoteActionGroup.add_actions(
            [
                ("File", None, _("File")),
                (
                    "SaveAsEvernote",  # name
                    "evernote",  # image
                    _("Save List as Evernote"),  # text
                    _("<Ctrl><Shift>S"),  # key-command
                    _("Save current shopping list as an Evernote checklist"),  # tooltip
                    self.save_as_evernote,  # callback
                ),
            ]
        )
        self.action_groups.append(shoppingListEvernoteActionGroup)

    def build_note(self):
        """
        Build the Evernote shopping list

        @return: str -- ENML formatted shopping list.
        """
        # get the shopping list.
        shopper = self.pluggable.get_shopper(self.pluggable.lst)
        org = shopper.organize(shopper.dic)

        note = ""
        for cat, items in org:
            # This is in ENML (evernote markup language)
            if not cat:
                cat = _("Unknown")
            note += "<div><h3>" + cat.title() + "</h3></div>\n"
            for itemName, amount in items:
                note += "<div><en-todo/>%s (%s)</div>\n" % (itemName, amount)
        return note

    def save_as_evernote(self, *args):
        """
        Build and post the shopping list to evernote.  If there are
        any failures and dialog box will be created to infrom the user.

        @raises EDAMUserException: Authentication failure posting to
                EverNote or a non-configuration related EDAMUserException.
        @raises Exception: Any other error is generating during posting.

        The errors get caught by gourmet and printed to the console, so we
        allow them propagate up, up the user has already been informed
        via dialog message.
        """
        prefs = Prefs.instance()
        if not prefs.get(PREF_DEVTOKEN, None) or not prefs.get(
            PREF_NOTEBOOK, DEFAULT_NOTEBOOK
        ):
            # No token provided, abort
            self.error_dialog(
                _("The Evernote Key and Notebook must be set in Preferences.")
            )

        # build evernote formatted shopping list.
        note = self.build_note()
        self.send_to_evernote(note, prefs)

    def send_to_evernote(self, note, prefs):
        """
        Do the actual sending of the shopping list to Evernote.

        @param note: str -- ENML formatted note
        @param prefs: gourmet.Prefs -- gourmet preferences.

        @raises EDAMUserException: Authentication failure posting to
                EverNote or a non-configuration related EDAMUserException.
        @raises Exception: Any other error is generating during posting.
        """
        # Send shopping list to evernote.
        try:
            everNote = shoppingList.ShoppingEverNote(
                prefs.get(PREF_DEVTOKEN, None),
                prefs.get(PREF_NOTEBOOK, DEFAULT_NOTEBOOK),
            )
            everNote.createShoppingList(note)
        except EDAMUserException as e:
            if e.errorCode == 2 and e.parameter == "Notebook.name":
                self.error_dialog(
                    _(
                        "The Evernote notebook can not be blank.  Please fix in Preferences."
                    )
                )
            elif e.errorCode == 2 and e.parameter == "authenticationToken":
                self.error_dialog(
                    _(
                        "Authentication Error: Has your key expired or is there a typo in your key?"
                    )
                )
                raise  # gourmet catches this and prints it to the console
            else:
                # Not a configuration issue, shouldn't happen.
                self.error_dialog(
                    _(
                        "Unexpected error communicating with Evernote (EDAMUserException)."
                    )
                )
                raise
        except Exception:
            # Unexpected catch all error to let the user know it failed.
            self.error_dialog(_("Unexpected error communicating with Evernote."))
            raise

    def error_dialog(self, messageStr):
        """
        Generates a modal MessageDialog with messageStr and shows it to
        the user.

        @param messageStr: str -- Message to show the user.
        """
        message = Gtk.MessageDialog(
            type=Gtk.MessageType.ERROR, buttons=Gtk.ButtonsType.OK
        )
        message.set_markup(messageStr)
        message.connect("response", self.close_dialog)
        message.run()

    @staticmethod
    def close_dialog(dialog, _):
        """
        Closes a dialog box.

        @param dialog: Gtk.MessageDialog -- the dialog to be closed.
        """
        dialog.destroy()
