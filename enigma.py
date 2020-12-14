from plugboard import Plugboard
from reflector import Reflector
from rotor import Rotor

ALPHABET = 'ABCDEFGHIJKLMNOPQRSTUVWXYZ'


class Enigma():
    def __init__(
        self,
        output,
        printing,
        stepping_enabled,
        rotors,
        starting_letters,
        ring_settings,
        reflector,
        letter_swaps
    ):

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
            with open('start_settings.txt', 'w') as writer:
                writer.writelines('Stepping Enabled:' +
                                  str(stepping_enabled)+'\n')
                writer.writelines('Rotors:'+str(rotors)+'\n')
                writer.writelines('Rotor Settings:'+str(starting_letters)+'\n')
                writer.writelines('Ring Settings:'+str(ring_settings)+'\n')
                writer.writelines('Reflector:'+str(reflector)+'\n')
                writer.writelines('Plugboard:'+str(letter_swaps)+'\n')

    def step_rotors(self, from_bombe):
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

    def encrypt(self, plaintext):
        if(self.printing_enabled):
            print()
            print()
            print('ENCRYPTING...')
            print()
        ciphertext = ''
        for i, plainletter in enumerate(plaintext):
            if (self.stepping_enabled):
                self.step_rotors(True)
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
            with open('start_settings.txt', 'a+') as writer:
                writer.write('Plaintext:'+plaintext+'\n')
                writer.write('Ciphertext:'+ciphertext+'\n')

        return ciphertext

    def to_string(self):
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
