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
