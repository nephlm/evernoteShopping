from evernote.api.client import EvernoteClient
import evernote.edam.type.ttypes as Types
import time

class EverNote(object):

    def __init__(self, devToken, testing=False):
        self._devToken = devToken
        self._noteStore = None
        self._testing = testing
        self._token = self.getAuthToken()
        #self._notStoreUrl = self.getNoteStore()
        if testing:
            self._client = EvernoteClient(token = self._token)
        else:
            self._client = EvernoteClient(token = self._token, sandbox=False)

    def getAuthToken(self):
        return self._devToken

    def getNoteStore(self):
        if not self._noteStore:
            self._noteStore = self._client.get_note_store()
        return self._noteStore


    def getNotebook(self, notebookName):
        """
        Gets the notebook object for the notebook named ``notebookName``.
        If it doesn't exist it will be created.

        @param notebookName: str -- The name of a evernote notebook.

        @returns: evernote.Notebook -- The evernote notebook object
                corresponding to ``notebookName``.
        """
        noteStore = self.getNoteStore()
        allNotebooks = noteStore.listNotebooks()
        try:
            return [x for x in allNotebooks if x.name == notebookName][0]
        except IndexError:
            notebook = Types.Notebook()
            notebook.name = notebookName
            return noteStore.createNotebook(notebook)

        # if notebookName not in [x.name for x in allNotebooks]:
        #     notebook = Types.Notebook()
        #     notebook.name = notebookName
        #     notebook = noteStore.createNotebook(notebook)
        #     return notebook
        # else:
        #     for notebook in allNotebooks:
        #         if notebook.name == notebookName:
        #             return notebook

    def createNote(self, title, noteString, notebookGuid):
        """
        Posts a note to evernote using ``title`` as the title and
        ``noteString`` as the body.  The note is posted to the
        notebook pointed to by ``notebookGuid``.

        @param title: str -- title of the note.
        @param noteString: str -- ENML formatted, but unwrapped note body.
        @param notebookGuid: str -- GUID of the notebook to post the note.

        @returns: evernote.Note -- The evernote object of the created note.
        """
        noteStore = self.getNoteStore()
        note = Types.Note()
        note.title = title
        note.content = self.wrapNoteString(noteString)
        if notebookGuid:
            note.notebookGuid = notebookGuid
        note = noteStore.createNote(note)
        if self._testing:
            print str(note)
        return note

    @staticmethod
    def wrapNoteString(noteBody):
        """
        Wraps ``noteBody`` in headers and ``<en-note>`` tags.

        @param noteBody: str -- ENML formatted note

        @returns: str -- completed/wrapped note.
        """
        body = "<?xml version=\"1.0\" encoding=\"UTF-8\"?>"
        body += "<!DOCTYPE en-note SYSTEM \"http://xml.evernote.com/pub/enml2.dtd\">"
        body += "<en-note>%s</en-note>" % noteBody
        return body.encode('ascii', 'xmlcharrefreplace')

class ShoppingEverNote(EverNote):
    """
    Shopping list specific subclass of ``EverNote``
    """
    def __init__(self, devToken, notebookName):
        """
        @param devToken: str -- The developer token to be used to
                access evernote.
        @param notebookName: str -- The name of the Notebook where
                shopping lists will posted.
        """
        super(ShoppingEverNote, self).__init__(devToken)
        self.notebookName = notebookName # 'Shopping Lists'
        self._notebookGuid = self.getShoppingListNotebook().guid

    def getShoppingListNotebook(self):
        """
        @returns: evernote.Notebook -- Notebook object corresponding
                to ``self.notebookName``
        """
        return self.getNotebook(self.notebookName)

    def createShoppingList(self, note):
        """
        High level shopping list posting function.  The title is
        derived from the current date.

        @param note: str -- ENML formatted note to be posted to
                evernote.
        """
        self.createNote('Shopping List for %s' % time.strftime('%x'),
                        note, self._notebookGuid)


# if __name__ == '__main__':
#     shoppingList = ShoppingEverNote()
#     notebook = shoppingList.getShoppingListNotebook()
#     print str((notebook.name, notebook.guid))
#     shoppingList.createShoppingList('foo')
