from gourmet.plugin import PrefsPlugin
from gourmet.prefs import get_prefs
import gtk
from gettext import gettext as _

from constants import PREF_NOTEBOOK, PREF_DEVTOKEN, DEFAULT_NOTEBOOK

class SL2EvernotePrefs (PrefsPlugin):
    """
    A preference pane for the evernote shopping lists plugin.
    It is where the user enters there evernote developer token and
    the name of the notebook where shopping lists should be
    saved.
    """

    label = _("Evernote Info")


    def __init__ (self, *args, **kwargs):
        """
        Sets up the Evernote preference pane.
        """
        # Create main widget
        self.widget = gtk.VBox()
        self.prefs = get_prefs()

        # developer token label and help
        dtHBox = gtk.HBox()
        devTokenLabel = gtk.Label(_('Developer Token'))
        devTokenLabel.set_alignment(xalign=0, yalign=0.5)
        dtHBox.pack_start(devTokenLabel, expand=False, fill=False, padding=5)

        dtEBox = gtk.EventBox()
        dtEBox.connect("button_press_event", self.press_help, 'devkey')
        img = gtk.Image()
        img.set_from_stock(gtk.STOCK_ABOUT, gtk.ICON_SIZE_MENU)
        dtEBox.add(img)
        dtEBox.set_visible_window(False)
        dtEBox.modify_bg(gtk.STATE_NORMAL, dtEBox.get_colormap().alloc_color("white"))
        dtHBox.pack_start(dtEBox, expand=False, fill=False, padding=5)
        self.widget.pack_start(dtHBox, expand=False, fill=False)

        # developer token entry
        self.devTokenEntry = gtk.Entry(max=0)
        self.devTokenEntry.set_text(self.prefs.get(PREF_DEVTOKEN, ''))
        self.devTokenEntry.connect('changed', self.save_change, PREF_DEVTOKEN)
        self.widget.pack_start(self.devTokenEntry, expand=False, fill=False)

        # Notebook label
        nbHBox = gtk.HBox()
        notebookLabel = gtk.Label(_('Shopping List Notebook'))
        notebookLabel.set_alignment(xalign=0, yalign=0.5)
        nbHBox.pack_start(notebookLabel, expand=False, fill=False, padding=5)

        nbEBox = gtk.EventBox()
        nbEBox.connect("button_press_event", self.press_help, 'notebook')
        img = gtk.Image()
        img.set_from_stock(gtk.STOCK_ABOUT, gtk.ICON_SIZE_MENU)
        nbEBox.add(img)
        nbEBox.set_visible_window(False)
        nbHBox.pack_start(nbEBox, expand=False, fill=False, padding=5)
        self.widget.pack_start(nbHBox, expand=False, fill=False)

        # Notebook entry
        self.notebookEntry = gtk.Entry(max=0)
        self.notebookEntry.set_text(self.prefs.get(PREF_NOTEBOOK, DEFAULT_NOTEBOOK))
        self.notebookEntry.connect('changed', self.save_change, PREF_NOTEBOOK)
        self.widget.pack_start(self.notebookEntry, expand=False, fill=False)

        # Show
        self.widget.set_border_width(12)
        self.widget.set_spacing(6)
        self.widget.show_all()

    def save_change(self, entry, key):
        """
        Update the prefs with a changed value and saves them to disk.
        Triggered when the user changes any of the entries.

        @param entry: gtk.Entry -- the entry that was changed.
        @param key: str -- The key to used to store the value in the
                    prefs.
        """
        self.prefs[key] = entry.get_text()
        self.prefs.save()

    def press_help(self, widget, event, key):
        """
        Displays a Help MessageDialog corresponding to the help icon
        pressed.

        @param widget: gtk.EventBox -- The event box that was clicked.
                    Not used.
        @param event: gtk.gdk.Event -- The event generated.  Not used.
        @param key: str -- User defined key set by connect()
        """
        print 'pressed %s', key

        if key == 'devkey':
            messageStr = "To access Evernote from an application that is "\
                    "not a webservice requires a misnamed 'Developer "\
                    "Token.'  You can get a Developer Token from " \
                    "\nhttps://www.evernote.com/api/DeveloperToken.action"
        else:
            messageStr = 'This is the name of the notebook where the '\
                        "shopping lists will be posted.  If it does not "\
                        "exist, it will be created."
        message = gtk.MessageDialog(type=gtk.MESSAGE_INFO, buttons=gtk.BUTTONS_OK)
        message.set_markup(messageStr)
        message.connect("response", self.close_dialog)
        message.run()

    @staticmethod
    def close_dialog(dialog, _):
        """
        Closes a dialog box.

        @param dialog: gtk.MessageDialog -- the dialog to be closed.
        """
        dialog.destroy()



