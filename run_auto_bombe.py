from menu_generator_1 import MenuGenerator
from bombe_2 import Bombe


def run(
    plain_crib,
    cipher_crib,
    top_rotor,
    middle_rotor,
    bottom_rotor,
    starting_letters,
    reflector,
    printing,
    output
):
    mg = MenuGenerator(plain_crib, cipher_crib, starting_letters)
    settings, connections, input_letter, _ = mg.get_bombe_settings()

    if output:
        with open('bombe_output.txt', 'a', newline='') as file:
            file.write(
                f'Rotors: {top_rotor}, {middle_rotor}, {bottom_rotor}\n')
            file.write(f'Reflector: {reflector}\n')
            file.write(f'Plain Crib: {plain_crib}\n')
            file.write(f'Cipher Crib: {cipher_crib}\n\n')
            file.write(f'Starting Letters: {starting_letters}\n')
            file.write(f'Input Letter: {input_letter}\n')
            file.write('Settings:\n')
            zipped_settings = zip(settings, connections)
            for line in zipped_settings:
                file.write(str(line)+'\n')
            file.write('\n')

    b = Bombe(
        top_rotor,
        middle_rotor,
        bottom_rotor,
        starting_letters,
        reflector,
        settings,
        connections,
        input_letter,
        printing,
        output
    )

    b.auto_run(plain_crib, cipher_crib)


if __name__ == '__main__':
    import sys
    plain_crib = sys.argv[1].upper()
    cipher_crib = sys.argv[2].upper()
    top_rotor = sys.argv[3].upper()
    middle_rotor = sys.argv[4].upper()
    bottom_rotor = sys.argv[5].upper()
    starting_letters = sys.argv[6].upper()
    reflector = sys.argv[7]
    printing = True if sys.argv[8] == 'True' else False
    output = True if sys.argv[9] == 'True' else False

    run(
        plain_crib,
        cipher_crib,
        top_rotor,
        middle_rotor,
        bottom_rotor,
        starting_letters,
        reflector,
        printing,
        output
    )
