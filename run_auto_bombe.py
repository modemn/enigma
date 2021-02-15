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
