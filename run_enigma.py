from enigma import Enigma
import reflector
import rotor

print('****************')
print('ENIGMA SIMULATOR')
print('****************')
print()

enigma = Enigma()

all_rotor_choices = rotor.get_rotor_choices()
print(
    'Select left, middle and right rotor from', all_rotor_choices)
print('Input each rotor number with a space in between')
print('Example input: I II III')
print('---------------------------------------')

# Collect rotor choices
choice = input()
rotors_choice = choice.split()

# Set the rotors on the enigma
enigma.set_rotors(rotors_choice)

print(enigma.l_rotor.name, enigma.m_rotor.name, enigma.r_rotor.name)

all_reflector_choices = reflector.get_reflector_choices()
print()
print()
print(
    'Select reflector from', all_reflector_choices)
print('Example input: B')
print('---------------------------------------')

# Collect reflector choice
choice = input()
reflector_choice = choice.split()

# Set the reflector on the enigma
enigma.set_reflector(reflector_choice[0])

print(enigma.reflector.name)

print()
print()
print('Input your message to encrpyt')
print('---------------------------------------')

message = input()
message = message.upper()

ciphertext = enigma.input(message)

print('Plaintext:', message)
print('Ciphertext:', ciphertext)
