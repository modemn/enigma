from enigma import Enigma
import reflector
import rotor

print('****************')
print('ENIGMA SIMULATOR')
print('****************')
print()

print('Would you like stepping enabled?')
print('Input Y or N')
print('---------------------------------------')

choice = input()
if (choice.upper() == 'Y'):
    choice = True
else:
    choice = False

enigma = Enigma(choice)

all_rotor_choices = rotor.get_rotor_choices()
print()
print()
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

print()
print()
print(
    'Enter starting letter settings for rotors')
print('Input each rotor number with a space in between')
print('Example input: A Y N')
print('---------------------------------------')

choice = input()
starting_letters = choice.split()

enigma.l_rotor.set_start(starting_letters[0])
enigma.m_rotor.set_start(starting_letters[1])
enigma.r_rotor.set_start(starting_letters[2])


print(enigma.l_rotor.current_letter_setting(),
      enigma.m_rotor.current_letter_setting(), enigma.r_rotor.current_letter_setting())

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
print('Input letter swaps in pairs with spaces in between')
print('Example input: AB NE LG')
print('---------------------------------------')

# Collect swap choices
choice = input()
swap_choice = choice.split()

# Set the swaps on the enigma's plugboard
enigma.set_swaps(swap_choice)

print()
print()
print('Input your message to encrpyt')
print('---------------------------------------')

message = input()
message = message.replace(" ", "").upper()

ciphertext = enigma.encrypt(message)

print('Plaintext:', message)
print('Ciphertext:', ciphertext)
