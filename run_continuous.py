from bombe_2_for_UI import Bombe


def run(
        ROTORS,
        REFLECTORS,
        starting_letters,
        input_letter,
        settings,
        connections,
        plain_crib,
        cipher_crib):
    i = 0
    rotor_combos = [(x, y, z)
                    for x in ROTORS for y in ROTORS for z in ROTORS if x != y if y != z if x != z]
    for top_rotor, middle_rotor, bottom_rotor in rotor_combos:
        for reflector in REFLECTORS:
            i += 1
            print(f'Settings {i}/180')
            print('******************BOMBE******************')
            print('Running the Bombe with the following settings:')
            print('Rotors:', top_rotor, middle_rotor, bottom_rotor)
            print('Reflector:', reflector)
            print('Starting Letters:', starting_letters)
            print('Input Letter:', input_letter)
            print('*****************************************')
            print()

            b = Bombe(
                top_rotor,
                middle_rotor,
                bottom_rotor,
                starting_letters,
                reflector,
                settings,
                connections,
                input_letter
            )

            print('RUNNING...')
            b.auto_run(plain_crib, cipher_crib)
