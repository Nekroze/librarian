"""Generic Card Class."""
__author__ = 'Taylor "Nekroze" Lawson'
__email__ = 'nekroze@eturnilnetwork.com'


class Card(object):
    """The card stores general information about the card.
     - code: the unique identifier for this card.
     - name: name of this card to be displayed.
     - abilities: dict of phase id's containing a list of action descriptors.
     - attributes: list of special details this card has.
     - info: dict of any information you would like.

    Card can be saved to, and loaded from, a string. Call `str()` on a Card
    instance or `.save_string()` on the instance. This will return a string
    that when evaluated using `eval()` can be unpacked into the Card
    constructor re-create that card. For example::
        original = Card(1, 'cool card')
        savestring = str(card)
        loaded = Card(*eval(savestring))
    """
    def __init__(self, code=None, name=None, loadstring=None):
        if loadstring is None:
            self.code = 0 if code is None else code
            self.name = '' if name is None else name
            self.abilities = {}
            self.attributes = []
            self.info = {}
        else:
            self.load_string(loadstring)

    def is_valid(self):
        """Returns True if code is not 0 and self.name is not ''."""
        return self.code != 0 and self.name != ''

    def has_attribute(self, attribute):
        """Return true if this card contains the given attribute."""
        return attribute in self.attributes

    def add_attribute(self, attribute):
        """Add the given attribute to this Card. Returns the length of
        attributes after addition.
        """
        self.attributes.append(attribute)
        return len(self.attributes)

    def get_abilities(self, phase):
        """Returns an ability list for the given phase ID."""
        return self.abilities[phase] if phase in self.abilities else None

    def add_ability(self, phase, ability):
        """Add the given ability to this Card under the given phase. Returns
        the length of the abilities for the given phase after the addition.
        """
        if phase not in self.abilities:
            self.abilities[phase] = []
        self.abilities[phase].append(ability)
        return len(self.abilities[phase])

    def get_info(self, key):
        """Return a value in the info for this card with the given key."""
        return self.info[key] if key in self.info else None

    def set_info(self, key, value, append=False):
        """Set any special info you wish to the given key. Will append rather
        then set if append is True. In the append case this will set key to a
        list if it currently is not set at all.

        If the info value for the given key is already a list then it will work
        as though append where True.
        """
        if append or key in self.info and isinstance(self.info[key], list):
            if key not in self.info:
                self.info[key] = []
            self.info[key].append(value)
        else:
            self.info[key] = value

    def save_string(self):
        """Converts the Card as is into a string capable of constructing a new
        Card identical to this one.
        """
        return str((self.code, self.name, self.abilities, self.attributes,
                    self.info))

    def load_string(self, string):
        """Takes a string as produced by ``Card.save_string()`` and sets this
        card instances information to the previously saved cards information.
        """
        args = eval(string)
        self.code, self.name = args[0:2]
        self.abilities, self.attributes, self.info = args[2:]

    def __eq__(self, other):
        """Return True if this card's code is the same as the other's code."""
        return self.code == other.code

    def __neq__(self, other):
        """Return True if this card's code is not the same as the other's
        code.
        """
        return self.code != other.code

    def __str__(self):
        """Called by str(MyCard)``. Returns a string that when given to
        ``eval()`` will produce a tuple that can be unpacked and given to the
        Card constructor to replicate this card.

        This is used for saving the card for later usage.
        """
        return self.save_string()

    def __repr__(self):
        """Called by ``repr(MyCard)``. Returns the string '<Card:#>' where '#'
        is replaced with the code for the card instance"""
        return '<Card:{0}>'.format(str(self.code))
