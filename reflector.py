REFLECTOR_DICT = {
    'A': {'name': 'A',
          'output': 'EJMZALYXVBWFCRQUONTSPIKHGD'},
    'B': {'name': 'B',
          'output': 'YRUHQSLDPXNGOKMIEBFZCWVJAT'},
    'C': {'name': 'C',
          'output': 'FVPJIAOYEDRZXWGCTKUQSBNMHL'}
}

ALPHABET = 'ABCDEFGHIJKLMNOPQRSTUVWXYZ'


def get_reflector_choices():
    return list(REFLECTOR_DICT.keys())


class Reflector:
    """A class to represent a reflector in the Engima machine.

    There are 3 reflectors currently defined - {A, B, C}

    Attributes
    ----------
    name: str
        The name of reflector.
    output: str
        The permutation of the alphabet reperesenting the reflection.
    printing: bool
        Determines whether to print the scrambling route to the terminal.

    Methods
    -------
    reflect(input)
        Reflects the letter.
    """

    def __init__(self, model, printing):
        """
        Parameters
        ----------
        model: int
            The name of reflector.
        printing: bool
            Determines whether to print the scrambling route to the terminal.
        """
        self.name = REFLECTOR_DICT[model]['name']
        self.output = REFLECTOR_DICT[model]['output']
        self.printing = printing

    def reflect(self, input):
        """Reflects the letter.

        Parameters
        ----------
        input: int
            The index in the alphabet of the input letter.

        Returns
        -------
        output: int
            The index in the alphabet of the reflected letter.
        """
        cipherletter = self.output[input]
        if (self.printing):
            print('->', cipherletter, '(reflector {})'.format(self.name))
        output = ALPHABET.find(cipherletter)
        return output
