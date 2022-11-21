from gourmand.plugin import PrefsPlugin
from gourmand.prefs import Prefs
from gi.repository import Gtk, Gdk
from gettext import gettext as _

from sl2evernote.constants import PREF_NOTEBOOK, PREF_DEVTOKEN, DEFAULT_NOTEBOOK


class SL2EvernotePrefs(PrefsPlugin):
    """
    A preference pane for the evernote shopping lists plugin.
    It is where the user enters there evernote developer token and
    the name of the notebook where shopping lists should be
    saved.
    """

    label = _("Evernote Info")

    def __init__(self, *args, **kwargs):
        """
        Sets up the Evernote preference pane.
        """
        # Create main widget
        self.widget = Gtk.VBox()
        self.prefs = Prefs.instance()

        # developer token label and help
        dtHBox = Gtk.HBox()
        devTokenLabel = Gtk.Label(_("Developer Token"))
        devTokenLabel.set_alignment(xalign=0, yalign=0.5)
        dtHBox.pack_start(devTokenLabel, expand=False, fill=False, padding=5)

        dtEBox = Gtk.EventBox()
        dtEBox.connect("button_press_event", self.press_help, "devkey")
        # img = Gtk.Image()
        img = Gtk.Image.new_from_icon_name("evernote", Gtk.IconSize.MENU)
        dtEBox.add(img)
        dtEBox.set_visible_window(False)
        dtEBox.modify_bg(
            Gtk.StateType.NORMAL,
            Gdk.color_parse("white")
            # Gtk.StateType.NORMAL, dtEBox.get_colormap().alloc_color("white")
        )
        dtHBox.pack_start(dtEBox, False, False, 5)
        self.widget.pack_start(dtHBox, False, False, 0)

        # developer token entry
        # self.devTokenEntry = Gtk.Entry(max=0)
        self.devTokenEntry = Gtk.Entry()
        self.devTokenEntry.set_text(self.prefs.get(PREF_DEVTOKEN, ""))
        self.devTokenEntry.connect("changed", self.save_change, PREF_DEVTOKEN)
        self.widget.pack_start(self.devTokenEntry, False, False, 0)

        # Notebook label
        nbHBox = Gtk.HBox()
        notebookLabel = Gtk.Label(_("Shopping List Notebook"))
        notebookLabel.set_alignment(xalign=0, yalign=0.5)
        nbHBox.pack_start(notebookLabel, expand=False, fill=False, padding=5)

        nbEBox = Gtk.EventBox()
        nbEBox.connect("button_press_event", self.press_help, "notebook")
        img = Gtk.Image.new_from_icon_name("evernote", Gtk.IconSize.MENU)
        nbEBox.add(img)
        nbEBox.set_visible_window(False)
        nbHBox.pack_start(nbEBox, False, False, 5)
        self.widget.pack_start(nbHBox, False, False, 0)

        # Notebook entry
        self.notebookEntry = Gtk.Entry()
        self.notebookEntry.set_text(self.prefs.get(PREF_NOTEBOOK, DEFAULT_NOTEBOOK))
        self.notebookEntry.connect("changed", self.save_change, PREF_NOTEBOOK)
        self.widget.pack_start(self.notebookEntry, False, False, 0)

        # Show
        self.widget.set_border_width(12)
        self.widget.set_spacing(6)
        self.widget.show_all()

    def save_change(self, entry, key):
        """
        Update the prefs with a changed value and saves them to disk.
        Triggered when the user changes any of the entries.

        @param entry: Gtk.Entry -- the entry that was changed.
        @param key: str -- The key to used to store the value in the
                    prefs.
        """
        self.prefs[key] = entry.get_text()
        self.prefs.save()

    def press_help(self, widget, event, key):
        """
        Displays a Help MessageDialog corresponding to the help icon
        pressed.

        @param widget: Gtk.EventBox -- The event box that was clicked.
                    Not used.
        @param event: Gtk.gdk.Event -- The event generated.  Not used.
        @param key: str -- User defined key set by connect()
        """
        print("pressed %s", key)

        if key == "devkey":
            messageStr = (
                "To access Evernote from an application that is "
                "not a webservice requires a misnamed 'Developer "
                "Token.'  You can get a Developer Token from "
                "\nhttps://www.evernote.com/api/DeveloperToken.action"
            )
        else:
            messageStr = (
                "This is the name of the notebook where the "
                "shopping lists will be posted.  If it does not "
                "exist, it will be created."
            )
        message = Gtk.MessageDialog(type=Gtk.MESSAGE_INFO, buttons=Gtk.BUTTONS_OK)
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
