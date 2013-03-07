"""Generic Card Class."""
__author__ = 'Taylor "Nekroze" Lawson'
__email__ = 'nekroze@eturnilnetwork.com'


class Card(object):
    """The card stores general information about the card.::
     - code: the unique identifier for this card.
     - name: name of this card to be displayed.
     - abilities: dict of phase id's containing a list of action descriptors.
     - attributes: list of special details this card has.
     - info: dict of any information you would like.

    Card can be saved to, and loaded from, a string. Call `str()` on a Card
    instance or `.save_string()` on the instance. This will return a string that
    when evaluated using `eval()` can be unpacked into the Card constructor to
    re-create that card. For example::
        original = Card(1, 'cool card')
        savestring = str(card)
        loaded = Card(*eval(savestring))
    """
    def __init__(self, code = None, name = None, abilities = None, 
                 attributes = None, info = None):
        self.code = 0 if code is None else code
        self.name = '' if name is None else name
        self.abilities = {} if abilities is None else abilities
        self.attributes = [] if attributes is None else attributes
        self.info = {} if info is None else info

    def save_string(self):
        return str((self.code, self.name, self.abilities, self.attributes,
        self.info))

    def __str__(self):
        return self.save_string()

    def __repr__(self):
        return '<Card:{0}>'.format(str(self.code))

    def is_valid(self):
        return self.code > 0 and self.name >= ''

    def has_attribute(self, attribute):
        return attribute in self.attributes

    def get_abilities(self, phase):
        return self.abilities[phase]

    def get_info(self, key):
        return self.info[key]
