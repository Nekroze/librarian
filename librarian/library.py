"""The Library class, an sqlite database of cards."""
__author__ = 'Taylor "Nekroze" Lawson'
__email__ = 'nekroze@eturnilnetwork.com'

import sqlite3
from .card import Card


class Library(object):
    """Library wraps an sqlite3 database that stores card codes and their
    corrosponding savestrings.

    Library also allows load and save hooks that allow a list of function to be
    called on each string as it is saved and loaded.
    """
    def __init__(self, dbname):
        self.dbname = dbname
        self.save_events = []
        self.load_events = []

    def create_db(self):
        """Create the CARDS table in the sqlite3 database."""
        with sqlite3.connect(self.dbname) as db:
            db.execute("CREATE TABLE CARDS(code NUMBER, card STRING)")

    def add_save_hook(self, func):
        """Add the given function to the save events.
        functions will be called in the order that they where added.

        Event functions should take and output a string.
        """
        self.save_events.append(func)

    def add_load_hook(self, func):
        """Add the given function to the load events.
        functions will be called in the order that they where added.

        Event functions should take and output a string.
        """
        self.load_events.append(func)

    def _prepare_save(self, savestring):
        """Run each save event on the given savestring and return the
        product.
        """
        for func in self.save_events:
            savestring = func(savestring)
        return savestring

    def _prepare_load(self, loadstring):
        """Run each load event on the given loadstring and return the
        product.
        """
        for func in self.load_events:
            loadstring = func(loadstring)
        return loadstring

    def load_card(self, code):
        """Load a card with the given code from the database. This calls each
        save event hook on the save string before commiting it to the database.
        """
        loadstring = None
        with sqlite3.connect(self.dbname) as db:
            loadstring = db.execute("SELECT card FROM CARDS WHERE code = ?",
                                     code)
        return Card(*eval(self._prepare_load(loadstring)))

    def save_card(self, card):
        """Save the given card to the database. This calls each save event hook
        on the save string before commiting it to the database.
        """
        savestring = self._prepare_save(str(card))
        with sqlite3.connect(self.dbname) as db:
            db.execute("INSERT INTO CARDS values (?, ?)", (card.code, savestring))
