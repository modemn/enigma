ROTOR_DICT = {
    'I': {
        'name': 'I',
        'output': 'EKMFLGDQVZNTOWYHXUSPAIBRCJ',
        'notch': 'Q'
    },
    'II': {
        'name': 'II',
        'output': 'AJDKSIRUXBLHWTMCQGZNPYFVOE',
        'notch': 'E'
    },
    'III': {
        'name': 'III',
        'output': 'BDFHJLCPRTXVZNYEIWGAKMUSQO',
        'notch': 'V'
    },
    'IV': {
        'name': 'IV',
        'output': 'ESOVPZJAYQUIRHXLNFTGKDCMWB',
        'notch': 'J'
    },
    'V': {
        'name': 'V',
        'output': 'VZBRGITYUPSDNHLXAWMJQOFECK',
        'notch': 'Z'
    }
}

ALPHABET = 'ABCDEFGHIJKLMNOPQRSTUVWXYZ'


def get_rotor_choices():
    return list(ROTOR_DICT.keys())


class Rotor:
    """A class to represnt a single rotor in the Engima machine.

    There are 5 rotors currently defined - {I, II, III, IV, V}

    Attributes
    ----------
    name: str
        The name of the rotor.
    output: str
        The permutation of the alphabet representing the scrambling.
    notch: str
        The letter which after stepping past will cause the next rotor to turnover.
    printing_enabled: bool 
        Determines whether to print the scrambling route to the terminal.
    pos: int
        The index of the alphabet representing the current letter of the rotor.
    ring_setting: int
        The number of letters to offset the scrambling by.

    Methods
    -------
    forward(input)
        Returns the index in the alphabet of the letter after scrambling right to left. 
    backward(input)
        Returns the index in the alphabet of the letter after scrambling right to left.
    current_letter_setting()
        Returns the letter the rotor is currently on.
    step()
        Steps the rotor one step.
    """

    def __init__(self, model, printing, start_letter, ring_setting):
        """
        Parameters
        ----------
        model: str
            The name of the rotor.
        printing: bool
            Determines whether to print the scrambling route to the terminal.
        start_letter: str
            The letter to start the rotor on.
        ring_setting: int
            The number of letters to offset the scrambling by.
        """
        self.name = ROTOR_DICT[model]['name']
        self.output = ROTOR_DICT[model]['output']
        self.notch = ROTOR_DICT[model]['notch']
        self.printing_enabled = printing
        self.pos = ALPHABET.find(start_letter)

        # Creating the new output alphabet given the ring settings
        self.ring_setting = ring_setting+1
        if (ring_setting != 0):
            dot_pos = self.output.find('A')
            new_wiring = ''
            for char in self.output:
                new_wiring += ALPHABET[(ALPHABET.find(char)+ring_setting) % 26]
            new_dot_pos = (dot_pos + ring_setting) % 26

            while not new_wiring[new_dot_pos] == ALPHABET[ring_setting]:
                new_wiring = new_wiring[-1:] + new_wiring[:-1]

            self.output = new_wiring

    def forward(self, input):
        """Scrambles the letter in the forward direction.

        Forward is determined to be the electrical signal travelling towards the reflector in the physical machine.

        Parameters
        ----------
        input: int
            The index in the alphabet of the input letter.

        Returns
        -------
        output: int
            The index in the alphabet of the scrambled letter.
        """
        output = (input+self.pos) % 26
        cipherletter = self.output[output]
        if(self.printing_enabled):
            print('->', cipherletter, '(forward through rotor {})'.format(self.name))
        output = (ALPHABET.find(cipherletter)-self.pos) % 26
        return output

    def backward(self, input):
        """Scrambles the letter in the backward direction.

        Backward is determined to be the electrical signal travelling away from the reflector in the physical machine.

        Parameters
        ----------
        input: int
            The index in the alphabet of the input letter.

        Returns
        -------
        output: int
            The index in the alphabet of the scrambled letter.
        """
        output = (input+self.pos) % 26
        output = self.output.find(ALPHABET[output])
        cipherletter = ALPHABET[output]
        if(self.printing_enabled):
            print('->', cipherletter,
                  '(backwards through rotor {})'.format(self.name))
        output = (output-self.pos) % 26
        return output

    def current_letter_setting(self):
        """Finds the current letter the rotor is on.

        This is equivalent to the outward showing letter on the front display on the physical machine.

        Parameters
        ----------
        None

        Returns
        -------
        ALPHABET[self.pos]: str
            The current letter the rotor is on.
        """
        return ALPHABET[self.pos]

    def step(self):
        """Steps the rotor.

        Also prints the name of the rotor if printing_enabled is True.

        Parameters
        ----------
        None

        Returns
        -------
        None
        """
        if(self.printing_enabled):
            print("Stepping rotor", self.name)
        self.pos = (self.pos+1) % 26
