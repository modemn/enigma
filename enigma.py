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

    def encrypt(self, plaintext):
        print('ENCRYPTING...')
        print()
        ciphertext = ''
        for i, plainletter in enumerate(plaintext):
            print('Plainletter', i+1, ':', plainletter)
            index = ALPHABET.find(plainletter)
            if (self.stepping_enabled):
                self.r_rotor.step()
            output = self.r_rotor.forward(index)
            output = self.m_rotor.forward(output)
            output = self.l_rotor.forward(output)
            output = self.reflector.reflect(output)
            output = self.l_rotor.backward(output)
            output = self.m_rotor.backward(output)
            output = self.r_rotor.backward(output)
            cipherletter = ALPHABET[int(output)]
            print('Cipherletter:', cipherletter)
            print()
            ciphertext += cipherletter

        return ciphertext
