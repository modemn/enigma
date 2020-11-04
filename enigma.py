from plugboard import Plugboard
from reflector import Reflector
from rotor import Rotor

ALPHABET = 'ABCDEFGHIJKLMNOPQRSTUVWXYZ'


class Enigma():
    def __init__(self, stepping_enabled):
        self.stepping_enabled = stepping_enabled

    def set_rotors(self, rotors):
        self.l_rotor = Rotor(rotors[0])
        self.m_rotor = Rotor(rotors[1])
        self.r_rotor = Rotor(rotors[2])

    def set_reflector(self, reflector):
        self.reflector = Reflector(reflector)

    def set_swaps(self, swap_choices):
        self.plugboard = Plugboard()
        for swap_choice in swap_choices:
            self.plugboard.set_swap(swap_choice[0], swap_choice[1])

    def step_rotors(self):
        middle_to_step = self.r_rotor.step()
        left_to_step = False
        if (middle_to_step):
            print('Stepping middle rotor')
            left_to_step = self.m_rotor.step()
        if (left_to_step):
            print('Stepping left rotor')
            self.l_rotor.step()
        print('Current rotor setting:', self.l_rotor.current_letter_setting(
        ), self.m_rotor.current_letter_setting(), self.r_rotor.current_letter_setting())

    def encrypt(self, plaintext):
        print('ENCRYPTING...')
        print()
        ciphertext = ''
        for i, plainletter in enumerate(plaintext):
            print('Plainletter', i+1, ':', plainletter)
            if (self.stepping_enabled):
                self.step_rotors()
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
            print('Cipherletter:', cipherletter)
            print()
            ciphertext += cipherletter

        return ciphertext
