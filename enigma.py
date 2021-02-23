from plugboard import Plugboard
from reflector import Reflector
from rotor import Rotor

ALPHABET = 'ABCDEFGHIJKLMNOPQRSTUVWXYZ'


class Enigma():
    """A class to represent and Enigma machine based on the Enigma M3.

    Attributes
    ----------
    output_enabled: bool 
        Determines whether to output a file named 'enigma_output.txt'.
    printing_enabled: bool
        Determines whether to print scrambling steps to the terminal.
    stepping_enabled: bool
        Determines whether to step the rotors after each letter encryption.
    starting_letters: list[str]
        The letters to start each rotor on. Rightmost rotor's letter specified first.
    l_rotor: Rotor
        The leftmost rotor.
    m_rotor: Rotor
        The middle rotor.
    r_rotor: Rotor
        The righmost rotor.
    reflector: Reflector
        The reflector.
    plugboard: Plugboard
        The plugboard.

    Methods
    -------
    step_rotors(from_bombe)
        Steps the rotors.
    encrypt(plaintext)
        Encrypts or decrypts the text through the Enigma.
    to_string()
        Contructs a string representation of the settings of the Enigma.
    """

    def __init__(
        self,
        output: bool,
        printing: bool,
        stepping_enabled: bool,
        rotors: list[str],
        starting_letters: list[str],
        ring_settings: list[str],
        reflector: str,
        letter_swaps: list[str]
    ):
        """
        Parameters
        ----------
        output: bool
            Determines whether to output a file named 'enigma_output.txt'.
        printing: bool
            Determines whether to print scrambling steps to the terminal.
        stepping_enabled: bool
            Determines whether to step the rotors after each letter encryption.
        rotors: list[str]
            The names of the rotors to use. Rightmost rotor specified first.
        starting_letters: list[str]
            The letters to start each rotor on. Rightmost rotor's letter specified first.
        ring_settings: list[str]
            The number of letters to set the ring settings to. Rightmost rotor's ring setting specified first.
        reflector: str
            The name of the reflector to use.
        letter_swaps: list[str]
            The pairs of swapped letters.
        """

        self.output_enabled = output
        self.printing_enabled = printing

        self.starting_letters = starting_letters

        self.stepping_enabled = stepping_enabled

        self.l_rotor = Rotor(
            rotors[0],
            self.printing_enabled,
            starting_letters[0],
            int(ring_settings[0])-1
        )
        self.m_rotor = Rotor(
            rotors[1],
            self.printing_enabled,
            starting_letters[1],
            int(ring_settings[1])-1
        )
        self.r_rotor = Rotor(
            rotors[2],
            self.printing_enabled,
            starting_letters[2],
            int(ring_settings[2])-1
        )

        self.reflector = Reflector(reflector, self.printing_enabled)

        self.plugboard = Plugboard(self.printing_enabled, letter_swaps)

        if (self.output_enabled):
            with open('enigma_output.txt', 'w') as writer:
                writer.writelines('Stepping Enabled:' +
                                  str(stepping_enabled)+'\n')
                writer.writelines('Rotors:'+str(rotors)+'\n')
                writer.writelines('Rotor Settings:'+str(starting_letters)+'\n')
                writer.writelines('Ring Settings:'+str(ring_settings)+'\n')
                writer.writelines('Reflector:'+str(reflector)+'\n')
                writer.writelines('Plugboard:'+str(letter_swaps)+'\n')

    def step_rotors(self, from_bombe: bool):
        """Steps the rotors.

        If the argument from_bombe is True, the stepping is done without regard for notches. Also prints the route if printing_enabled is True.

        Parameters
        ----------
        from_bombe: bool 
            Whether the instruction for stepping has come from a Bombe or this Enigma.

        Returns
        -------
        None
        """
        if (not from_bombe):
            r_notched = (self.r_rotor.current_letter_setting()
                         == self.r_rotor.notch)
            m_notched = (self.m_rotor.current_letter_setting()
                         == self.m_rotor.notch)

            self.r_rotor.step()

            if (r_notched and (not m_notched)):
                self.m_rotor.step()
            elif ((r_notched and m_notched) or (m_notched)):
                self.l_rotor.step()
                self.m_rotor.step()
        elif(from_bombe):
            self.l_rotor.step()
            if (self.l_rotor.current_letter_setting() == self.starting_letters[0]):
                self.m_rotor.step()
                if (self.m_rotor.current_letter_setting() == self.starting_letters[1]):
                    self.r_rotor.step()

        if (self.printing_enabled):
            print('Current rotor setting:', self.l_rotor.current_letter_setting(
            ), self.m_rotor.current_letter_setting(), self.r_rotor.current_letter_setting())

    def encrypt(self, plaintext: str):
        """Encrypts or decrypts the text through the Enigma.

        Although named 'encrypt', this method can be used to decrypt too since the operations are identical. Also prints the plain and cipher letter output if printing_enabled is True. Also outputs the plain and cipher text to a file if output_enabled is True.

        Parameters
        ----------
        plaintext: str
            The text to encrypt or decrypt

        Returns
        -------
        ciphertext: str
            The text after encryption or decryption of the plaintext.
        """
        if(self.printing_enabled):
            print()
            print()
            print('ENCRYPTING...')
            print()
        ciphertext = ''
        for i, plainletter in enumerate(plaintext):
            if (self.stepping_enabled):
                self.step_rotors(False)
            if (self.printing_enabled):
                print('Plainletter', i+1, ':', plainletter)
            output = self.plugboard.swap(plainletter)
            output = self.r_rotor.forward(output)
            output = self.m_rotor.forward(output)
            output = self.l_rotor.forward(output)
            output = self.reflector.reflect(output)
            output = self.l_rotor.backward(output)
            output = self.m_rotor.backward(output)
            output = self.r_rotor.backward(output)
            cipherletter = ALPHABET[int(output)]
            output = self.plugboard.swap(cipherletter)
            cipherletter = ALPHABET[int(output)]
            if (self.printing_enabled):
                print('Cipherletter:', cipherletter)
                print()
            ciphertext += cipherletter

        if(self.output_enabled):
            with open('enigma_output.txt', 'a+') as writer:
                writer.write('Plaintext:'+plaintext+'\n')
                writer.write('Ciphertext:'+ciphertext+'\n')

        return ciphertext

    def to_string(self):
        """Contructs a string representation of the settings of the Enigma.

        Parameters
        ----------
        None

        Returns
        -------
        output: str
            A string of the rotors, reflector and plugboard settings of the Enigma.
        """
        output = ''
        output += 'Left Rotor: '+self.l_rotor.name + ' ' + \
            self.l_rotor.current_letter_setting()+' '+str(self.l_rotor.ring_setting)+'\n'
        output += 'Middle Rotor: '+self.m_rotor.name + ' ' + \
            self.m_rotor.current_letter_setting()+' '+str(self.m_rotor.ring_setting)+'\n'
        output += 'Right Rotor: '+self.r_rotor.name + ' ' + \
            self.r_rotor.current_letter_setting()+' '+str(self.r_rotor.ring_setting)+'\n'
        output += 'Reflector: '+self.reflector.name+'\n'
        output += 'Plugboard: '+self.plugboard.output+'\n'
        return output
