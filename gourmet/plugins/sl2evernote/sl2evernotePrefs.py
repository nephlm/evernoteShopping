from gourmet.plugin import PrefsPlugin
from gourmet.prefs import get_prefs
import gtk
from gettext import gettext as _

from constants import PREF_NOTESTORE, PREF_DEVTOKEN

class SL2EvernotePrefs (PrefsPlugin):

    label = _("Evernote Info")
    explainText = "To access Evernote from an application that is "\
                    "not a webservice requires a misnamed 'Developer "\
                    "Token.'  You can get a Developer Token from "
    url = "https://www.evernote.com/api/DeveloperToken.action"


    def __init__ (self, *args, **kwargs):
        # Create main widget
        self.widget = gtk.VBox()
        self.prefs = get_prefs()

        devTokenLabel = gtk.Label(_('Developer Token'))
        devTokenLabel.set_alignment(xalign=0, yalign=0.5)
        self.widget.pack_start(devTokenLabel, expand=False, fill=False)

        self.devTokenEntry = gtk.Entry(max=0)
        self.devTokenEntry.set_text(self.prefs.get(PREF_DEVTOKEN, ''))
        self.devTokenEntry.connect('changed', self.change_token)
        self.widget.pack_start(self.devTokenEntry, expand=False, fill=False)

        noteStoreLabel = gtk.Label(_('NoteStore URL'))
        noteStoreLabel.set_alignment(xalign=0, yalign=0.5)
        self.widget.pack_start(noteStoreLabel, expand=False, fill=False)

        self.noteStoreEntry = gtk.Entry(max=0)
        self.noteStoreEntry.set_text(self.prefs.get(PREF_NOTESTORE, ''))
        self.noteStoreEntry.connect('changed', self.change_store)
        self.widget.pack_start(self.noteStoreEntry, expand=False, fill=False)

        self.widget.set_border_width(12)
        self.widget.set_spacing(6)
        self.widget.show_all()

    def change_token(self, _):
        self.prefs[PREF_DEVTOKEN] = self.devTokenEntry.get_text()

        if not self.noteStoreEntry.get_text():
            try:
                shard = self.devTokenEntry.get_text().split(':')[0].split('=')[1]
                self.noteStoreEntry.set_text('https://www.evernote.com/shard/%s/notestore' % shard)
                self.prefs[PREF_NOTESTORE] = self.noteStoreEntry.get_text()
            except IndexError:
                # dev token is incomplete or has changed format
                pass
        self.prefs.save()

    def change_store(self, _):
        self.prefs[PREF_NOTESTORE] = self.noteStoreEntry.get_text()
        self.prefs.save()
