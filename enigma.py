from plugboard import Plugboard
from reflector import Reflector
from rotor import Rotor
from termcolor import colored
import time

ALPHABET = 'ABCDEFGHIJKLMNOPQRSTUVWXYZ'


class Enigma():
    """A class to represent an Enigma machine based on the Enigma M3.

    Attributes
    ----------
    output_enabled: bool 
        Determines whether to output a file named 'enigma_output.txt'.
    printing_enabled: bool
        Determines whether to print scrambling steps to the terminal.
    stepping_enabled: bool
        Determines whether to step the rotors after each letter encryption.
    starting_letters: list[str]
        The letters to start each rotor on. Leftmost rotor's letter specified first.
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
            The names of the rotors to use. Leftmost rotor specified first.
        starting_letters: list[str]
            The letters to start each rotor on. Leftmost rotor's letter specified first.
        ring_settings: list[str]
            The number of letters to set the ring settings to. Leftmost rotor's ring setting specified first.
        reflector: str
            The reflector's name.
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
            with open('enigma_output.txt', 'w') as file:
                file.writelines('Stepping Enabled:' +
                                str(stepping_enabled)+'\n')
                file.writelines('Rotors:'+str(rotors)+'\n')
                file.writelines('Rotor Settings:'+str(starting_letters)+'\n')
                file.writelines('Ring Settings:'+str(ring_settings)+'\n')
                file.writelines('Reflector:'+str(reflector)+'\n')
                file.writelines('Plugboard:'+str(letter_swaps)+'\n')

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
                         in list(self.r_rotor.notch))
            m_notched = (self.m_rotor.current_letter_setting()
                         in list(self.m_rotor.notch))

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
        start_time = time.time()
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

        elapsed_time = time.time() - start_time

        if (self.printing_enabled):
            print(f'Time taken to encrypt: {elapsed_time} seconds')

        if(self.output_enabled):
            with open('enigma_output.txt', 'a+') as file:
                file.write('Plaintext:'+plaintext+'\n')
                file.write('Ciphertext:'+ciphertext+'\n')
                file.write(f'Time taken: {elapsed_time} seconds')

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


if __name__ == '__main__':
    import reflector
    import rotor
    import random
    import ast
    from termcolor import colored

    def run_with_user_input():
        print()
        print()
        print('****************')
        print('ENIGMA SIMULATOR')
        print('****************')

        print()
        print()
        print('Would you like stepping enabled?')
        print('Input Y or N (default is Y)')
        print(colored('---------------------------------------', 'blue'))

        choice = input()
        if ((choice.upper() == 'Y') or (len(choice) == 0)):
            stepping_choice = True
        else:
            stepping_choice = False

        all_rotor_choices = rotor.get_rotor_choices()
        print()
        print()
        print(
            'Select left, middle and right rotor from', all_rotor_choices)
        print('Input each rotor number with a space in between')
        print('Example input: II V IV (Default is I II III)')
        print(colored('---------------------------------------', 'blue'))

        # Collect rotor choices
        choice = input()
        if (len(choice) == 0):
            rotors_choice = ['I', 'II', 'III']
        else:
            rotors_choice = choice.split()

        print()
        print()
        print(
            'Enter starting letter settings for rotors')
        print('Input each rotor\'s starting letter with a space in between')
        print('Example input: Q Y N (Default is A A A)')
        print(colored('---------------------------------------', 'blue'))

        choice = input()
        choice = choice.upper()
        if (len(choice) == 0):
            starting_letters_choice = ['A', 'A', 'A']
        else:
            starting_letters_choice = choice.split()

        print()
        print()
        print(
            'Enter ring settings for rotors')
        print('Input each rotor\'s offset number (max 26) with a space in between')
        print('Example input: 4 17 8 (Default is 1 1 1)')
        print(colored('---------------------------------------', 'blue'))

        choice = input()
        if(len(choice) == 0):
            ring_settings = ['1', '1', '1']
        else:
            ring_settings = choice.split()

        all_reflector_choices = list(reflector.REFLECTOR_DICT.keys())
        print()
        print()
        print(
            'Select reflector from', all_reflector_choices)
        print('Example input: B (Default is B)')
        print(colored('---------------------------------------', 'blue'))

        # Collect reflector choice
        choice = input()
        choice = choice.upper()
        if (len(choice) == 0):
            reflector_choice = 'B'
        else:
            reflector_choice = choice.split()[0]

        print()
        print()
        print('Input letter swaps in pairs with spaces in between')
        print('Example input: AB NE LG (Default is no swaps)')
        print(colored('---------------------------------------', 'blue'))

        # Collect swap choices
        choice = input()
        choice = choice.upper()
        swap_choices = choice.split()

        print()
        print()
        print('Would you like scrambling path printing?')
        print('Input Y or N (Default is Y)')
        print(colored('---------------------------------------', 'blue'))

        choice = input()
        if ((choice.upper() == 'Y') or (len(choice) == 0)):
            printing_choice = True
        else:
            printing_choice = False

        print()
        print()
        print('Would you like the Engima settings to be saved to a file?')
        print('Input Y or N (Default is Y)')
        print(colored('---------------------------------------', 'blue'))

        choice = input()
        if ((choice.upper() == 'Y') or (len(choice) == 0)):
            output_choice = True
        else:
            output_choice = False

        enigma = Enigma(output_choice, printing_choice, stepping_choice, rotors_choice, starting_letters_choice,
                        ring_settings, reflector_choice, swap_choices)

        print()
        print()
        print(colored('Enigma Starting Settings:', 'green'))
        print(colored('*************************', 'green'))
        print('Stepping Enabled:', enigma.stepping_enabled)
        print('Rotors Selected:', enigma.l_rotor.name,
              enigma.m_rotor.name, enigma.r_rotor.name)
        print('Rotor Setting:', enigma.l_rotor.current_letter_setting(),
              enigma.m_rotor.current_letter_setting(), enigma.r_rotor.current_letter_setting())
        print('Rotor Ring Settings:', enigma.l_rotor.ring_setting,
              enigma.m_rotor.ring_setting, enigma.r_rotor.ring_setting)
        print('Reflector Selected:', enigma.reflector.name)
        print('Swapped Letters:', swap_choices)
        print('Scrambling Path Printing:', enigma.printing_enabled)
        print(colored('*************************', 'green'))

        print()
        print()
        print('Input your message to encrpyt')
        print(colored('---------------------------------------', 'blue'))

        message = input()
        message = message.replace(" ", "").upper()

        ciphertext = enigma.encrypt(message)

        print()
        print(colored('*************************', 'red'))
        print('Plaintext:', message)
        print('Ciphertext:', ciphertext)
        print(colored('*************************', 'red'))
        print()

    def run_from_file():
        print()
        print()
        print('****************')
        print('ENIGMA SIMULATOR')
        print('****************')

        print()
        print()
        print('Please enter the name of the file')
        print(colored('---------------------------------------', 'blue'))
        filename = input()+'.txt'

        try:
            with open(filename, 'r') as reader:
                lines = reader.readlines()
                opts = []
                for line in lines:
                    opts.append(line[line.find(':')+1:-1])
        except:
            print()
            print(colored('Could not find a file with that name', 'red'))
            return

        stepping_enabled = ast.literal_eval(opts[0])
        rotors = ast.literal_eval(opts[1])
        rotor_settings = ast.literal_eval(opts[2])
        ring_settings = ast.literal_eval(opts[3])
        reflector = opts[4]
        plugboard = ast.literal_eval(opts[5])
        plaintext = opts[6]

        enigma = Enigma(
            # TODO: CHANGE THIS TO FALSE AFTER EXPERIMENTS ARE DONE
            True,
            False,
            stepping_enabled,
            rotors,
            rotor_settings,
            ring_settings,
            reflector,
            plugboard
        )

        ciphertext = enigma.encrypt(plaintext)
        print()
        print(colored('*************************', 'red'))
        print('Plaintext:', plaintext)
        print('Ciphertext:', ciphertext)
        print(colored('*************************', 'red'))
        print()

    def run_random():
        print()
        print()
        print('****************')
        print('ENIGMA SIMULATOR')
        print('****************')

        print()
        print()
        print('Would you like scrambling path printing?')
        print('Input Y or N (Default is Y)')
        print(colored('---------------------------------------', 'blue'))

        choice = input()
        if ((choice.upper() == 'Y') or (len(choice) == 0)):
            printing_choice = True
        else:
            printing_choice = False

        print()
        print()
        print('Would you like the Engima settings to be saved to a file?')
        print('Input Y or N (Default is Y)')
        print(colored('---------------------------------------', 'blue'))

        choice = input()
        if ((choice.upper() == 'Y') or (len(choice) == 0)):
            output_choice = True
        else:
            output_choice = False

        print()
        print()
        print('Please enter the plaintext you want to encipher')
        print('-----------------------------------------------')

        plain = input().replace(' ', '').upper()

        rotors = random.sample(['I', 'II', 'III', 'IV', 'V'], k=3)
        starting_letters = random.choices(list(ALPHABET), k=3)
        ring_settings = random.choices(list(str(k) for k in range(1, 27)), k=3)
        reflector = random.sample(['A', 'B', 'C'], k=1)[0]
        a_copy = list(ALPHABET)[:]
        random.shuffle(a_copy)
        steckers = [''.join(a_copy[i*2: (i+1)*2])
                    for i in range(random.randint(5, 10))]

        enigma = Enigma(
            output_choice,
            printing_choice,
            True,
            rotors,
            starting_letters,
            ring_settings,
            reflector,
            steckers
        )

        print()
        print()
        print('Enigma Starting Settings:')
        print('*************************')
        print('Rotors Selected:', enigma.l_rotor.name,
              enigma.m_rotor.name, enigma.r_rotor.name)
        print('Rotor Setting:', enigma.l_rotor.current_letter_setting(),
              enigma.m_rotor.current_letter_setting(), enigma.r_rotor.current_letter_setting())
        print('Rotor Ring Settings:', enigma.l_rotor.ring_setting,
              enigma.m_rotor.ring_setting, enigma.r_rotor.ring_setting)
        print('Reflector Selected:', enigma.reflector.name)
        print('Swapped Letters:', steckers)
        print('*************************')

        cipher = enigma.encrypt(plain)

        print()
        print(colored('*************************', 'red'))
        print('Plaintext:', plain)
        print('Ciphertext:', cipher)
        print(colored('*************************', 'red'))
        print()

    print()
    print('1. Run an Enigma with user input')
    print('2. Run an Enigma from a file')
    print('3. Run a random Enigma')
    print()
    print('Enter the number of the option you would like')
    print(colored('---------------------------------------', 'blue'))
    choice = int(input())

    if choice == 1:
        run_with_user_input()
    elif choice == 2:
        run_from_file()
    elif choice == 3:
        run_random()
