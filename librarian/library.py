"""The Library class, an sqlite database of cards."""
__author__ = 'Taylor "Nekroze" Lawson'
__email__ = 'nekroze@eturnilnetwork.com'
from functools import partial
import sqlite3
from .card import Card


FIELDS = ("code", "name", "abilities", "attributes", "info")


class Library(object):
    """
    Library wraps an sqlite3 database that stores card codes and their
    corrosponding savestrings.

    Library also allows load and save hooks that allow a list of function to be
    called on each string as it is saved and loaded.
    """
    def __init__(self, dbname, cachelimit=100):
        self.dbname = dbname
        self.save_chain = []
        self.load_chain = []
        self.cachelimit = cachelimit
        self.card_cache = {}
        self.card_cache_list = []

    def cached(self, code):
        """Return True if there is a card for the given code in the cache."""
        return code in self.card_cache[code]

    def cache_card(self, card):
        """
        Cache the card for faster future lookups. Removes the oldest card
        when the card cache stores more cards then this libraries cache limit.
        """
        code = card.code
        self.card_cache[code] = card
        if code in self.card_cache_list:
            self.card_cache_list.remove(code)
        self.card_cache_list.append(code)

        if len(self.card_cache_list) > self.cachelimit:
            del self.card_cache[self.card_cache_list.pop(0)]

    def create_db(self):
        """Create the CARDS table in the sqlite3 database."""
        with sqlite3.connect(self.dbname) as carddb:
            carddb.execute("CREATE TABLE CARDS(code NUMBER, name STRING,
abilities STRING, attributes STRING, info STRING)")

    def load_card(self, code, cache=True):
        """
        Load a card with the given code from the database. This calls each
        save event hook on the save string before commiting it to the database.

        Will cache each resulting card for faster future lookups with this
        method while respecting the libraries cache limit. However only if the
        cache argument is True.
        """
        card = self.card_cache.get(code, None)
        if card is None:
            with sqlite3.connect(self.dbname) as carddb:
                loadstring = carddb.execute(
                    "SELECT * FROM CARDS WHERE code = ?", code)
                loadrow = loadstring.fetchone()
                loaddict = dict(zip(FIELDS, loadrow))
                card = Card(loaddict=loaddict)
            if cache:
                self.cache_card(card)
        return card

    def save_card(self, card, cache=False):
        """
        Save the given card to the database. This calls each save event hook
        on the save string before commiting it to the database.
        """
        if cache:
            self.cache_card(card)
        savedict = card.save()
        with sqlite3.connect(self.dbname) as carddb:
            carddb.execute("INSERT INTO CARDS VALUES(?, ?, ?, ?, ?)",
                           [cardict[key] for key in FIELDS])

    def connection(self):
        """Connect to the underlying database and return the connection."""
        return sqlite3.connect(self.dbname)
