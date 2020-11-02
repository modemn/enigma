from reflector import Reflector
from rotor import Rotor


class Enigma():
    def set_rotors(self, rotors):
        self.l_rotor = Rotor(rotors[0])
        self.m_rotor = Rotor(rotors[1])
        self.r_rotor = Rotor(rotors[2])

    def set_reflector(self, reflector):
        self.reflector = Reflector(reflector)

    def input(self, plaintext):
        ciphertext = ''
        for plainletter in plaintext:
            cipherletter = self.r_rotor.forward(plainletter)
            cipherletter = self.m_rotor.forward(cipherletter)
            cipherletter = self.l_rotor.forward(cipherletter)
            cipherletter = self.reflector.reflect(cipherletter)
            cipherletter = self.l_rotor.backward(cipherletter)
            cipherletter = self.m_rotor.backward(cipherletter)
            cipherletter = self.r_rotor.backward(cipherletter)
            ciphertext += cipherletter

        return ciphertext
