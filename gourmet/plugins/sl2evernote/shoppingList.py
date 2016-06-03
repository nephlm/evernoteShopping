from evernote.api.client import EvernoteClient
import evernote.edam.type.ttypes as Types
import time

class EverNote(object):

    def __init__(self, devToken, noteStoreUrl, testing=False):
        self._devToken = devToken
        # self._noteStoreUrl = noteStoreUrl
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

    # def getNoteStoreUrl(self):
    #     return self._noteStoreUrl

    def getNoteStore(self):
        if not self._noteStore:
            self._noteStore = self._client.get_note_store()
        return self._noteStore


    def getNotebook(self, notebookName):
        noteStore = self.getNoteStore()
        allNotebooks = noteStore.listNotebooks()
        if notebookName not in [x.name for x in allNotebooks]:
            notebook = Types.Notebook()
            notebook.name = notebookName
            notebook = noteStore.createNotebook(notebook)
            return notebook
        else:
            for notebook in allNotebooks:
                if notebook.name == notebookName:
                    return notebook

    def createNote(self, title, noteString, notebookGuid):
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
        body = "<?xml version=\"1.0\" encoding=\"UTF-8\"?>"
        body += "<!DOCTYPE en-note SYSTEM \"http://xml.evernote.com/pub/enml2.dtd\">"
        body += "<en-note>%s</en-note>" % noteBody
        body = body.encode('ascii', 'xmlcharrefreplace')
        return body

class ShoppingEverNote(EverNote):
    def __init__(self, devToken, noteStore, notebookName):
        super(ShoppingEverNote, self).__init__(devToken, noteStore)
        self.notebookName = notebookName # 'Shopping Lists'
        self._notebookGuid = self.getShoppingListNotebook().guid

    def getShoppingListNotebook(self):
        return self.getNotebook(self.notebookName)

    def createShoppingList(self, note):
        self.createNote('Shopping List for %s' % time.strftime('%x'), note, self._notebookGuid)


if __name__ == '__main__':
    shoppingList = ShoppingEverNote()
    #everNote.createNote('a body')
    notebook = shoppingList.getShoppingListNotebook()
    print str((notebook.name, notebook.guid))
    shoppingList.createShoppingList('foo')
