ALPHABET = 'ABCDEFGHIJKLMNOPQRSTUVWXYZ'


class Plugboard():
    """A class to represnt the plugboard in the Engima machine.

    Attributes
    ----------
    output: str
        The permutation of the alphabet representing the scrambling.
    printing: bool 
        Determines whether to print the scrambling route to the terminal.

    Methods
    -------
    set_swap(letter_1, letter_2)
        Construcs the output alphabet by swapping the letters in the alphabet and saving it.
    swap(input)
        Swaps the letter.
    """

    def __init__(self, printing, letter_swaps):
        """
        Parameters
        ----------
        output: str
            The permutation of the alphabet reperesenting the swapping. Defaults to the english alphabet.
        printing: bool
            Determines whether to print the scrambling route to the terminal.
        """
        self.output = ALPHABET
        self.printing = printing
        if (len(letter_swaps) != 0):
            for letter_swap in letter_swaps:
                self.set_swap(letter_swap[0], letter_swap[1])

    def set_swap(self, letter_1, letter_2):
        """Construcs the output alphabet by swapping the letters in the alphabet.

        Parameters
        ----------
        letter_1: str
            The first letter to swap.
        letter_2: str
            The second letter to swap.

        Returns
        -------
        None
        """
        index_1 = ALPHABET.find(letter_1)
        index_2 = ALPHABET.find(letter_2)
        output_list = list(self.output)
        output_list[index_1], output_list[index_2] = output_list[index_2], output_list[index_1]
        self.output = "".join(output_list)

    def swap(self, input):
        """Swaps the letter.

        Parameters
        ----------
        input: str
            The letter to get swapped.

        Returns
        -------
        output: int
            The index in the alphabet of the swapped letter.
        """
        index = ALPHABET.find(input)
        cipherletter = self.output[index]
        if (self.printing):
            print('->', cipherletter, '(Through pluboard)')
        output = ALPHABET.find(cipherletter)
        return output
