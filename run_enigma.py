from enigma import Enigma
import reflector
import rotor
from termcolor import colored

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

enigma = Enigma(stepping_choice)

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

# Set the rotors on the enigma
enigma.set_rotors(rotors_choice)

print()
print()
print(
    'Enter starting letter settings for rotors')
print('Input each rotor\'s starting letter with a space in between')
print('Example input: Q Y N (Default is A A A)')
print(colored('---------------------------------------', 'blue'))

choice = input()
choice = choice.upper()
starting_letters = choice.split()

enigma.set_rotors_start(starting_letters)

print()
print()
print(
    'Enter ring settings for rotors')
print('Input each rotor\'s offset number (max 26) with a space in between')
print('Example input: 4 17 8 (Default is 1 1 1)')
print(colored('---------------------------------------', 'blue'))

choice = input()
ring_settings = choice.split()

enigma.set_ring_settings(ring_settings)

all_reflector_choices = reflector.get_reflector_choices()
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
    reflector_choice = ['B']
else:
    reflector_choice = choice.split()

# Set the reflector on the enigma
enigma.set_reflector(reflector_choice[0])

print()
print()
print('Input letter swaps in pairs with spaces in between')
print('Example input: AB NE LG (Default is no swaps)')
print(colored('---------------------------------------', 'blue'))

# Collect swap choices
choice = input()
choice = choice.upper()
swap_choices = choice.split()

# Set the swaps on the enigma's plugboard
enigma.set_swaps(swap_choices)

print()
print()
print(colored('Enigma Starting Settings:', 'green'))
print(colored('*************************', 'green'))
print('Stepping Enabled:', enigma.stepping_enabled)
print('Rotors Selected:', enigma.l_rotor.name,
      enigma.m_rotor.name, enigma.r_rotor.name)
print('Rotor Setting:', enigma.l_rotor.current_letter_setting(),
      enigma.m_rotor.current_letter_setting(), enigma.r_rotor.current_letter_setting())
print('Rotor ring settings:', enigma.l_rotor.ring_setting,
      enigma.m_rotor.ring_setting, enigma.r_rotor.ring_setting)
print('Reflector Selected:', enigma.reflector.name)
print('Swapped letters:', swap_choices)
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
