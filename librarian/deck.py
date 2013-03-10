"""Generic Card Class."""
__author__ = 'Taylor "Nekroze" Lawson'
__email__ = 'nekroze@eturnilnetwork.com'

import random


class Deck(object):
    """A collection of possibly recuring cards."""
    def __init__(self, library=None, cards=None):
        self.library = library
        self.cards = cards if cards is not None else []

    def remaining(self):
        """Returns the number of remaining cards in the deck."""
        return len(self.cards)

    def shuffle(self):
        """Sort the cards in the deck into a random order.."""
        self.cards = random.shuffle(self.cards)

    def get_card(self, index=0, cache=True, remove=True):
        """Retreive a card any number of cards from the top. Returns a
        ``Librarian.Card`` object loaded from a library if one is specified
        otherwise just return its code.

        If cache is set to True (the default) it will tell the library to cache
        the returned card for faster future lookups.

        If remove is true then the card will be removed from the deck and
        returned.
        """
        if len(self.cards) < index:
            return None
        retreiver = self.cards.pop if remove else self.cards.__getitem__

        if self.library is None:
            return retreiver(index)
        else:
            return self.library.load_card(retreiver(index), cache)

    def get_top_card(self, cache=True, remove=True):
        """Return the card on the top of the deck as a ``Librarian.Card`` using
        the the decks ``.get_card`` method and passes along cache and remove
        arguments.
        """
        return self.get_card(0, cache, remove)

    def get_top_cards(self, number=1, cache=True, remove=True):
        """Retreive the top number of cards as ``Librarian.Card`` objects in a
        list in order of top to bottom most card. Uses the decks ``.get_card``
        and passes along the cache and remove arguments.
        """
        output = []
        for index in range(number):
            output.append(self.get_card(index, cache, remove))
        return output
