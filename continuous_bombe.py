import sys
import time
import run_auto_bombe

ROTORS = ['I', 'II', 'III', 'IV', 'V']
REFLECTORS = ['A', 'B', 'C']

plain_crib = sys.argv[1].upper()
cipher_crib = sys.argv[2].upper()
reflector = sys.argv[3].upper()
starting_letters = sys.argv[4].upper()


if __name__ == '__main__':
    starttime = time.time()
    rotor_combos = [
        (x, y, z) for x in ROTORS for y in ROTORS for z in ROTORS if x != y if y != z if x != z]
    for top_rotor, middle_rotor, bottom_rotor in rotor_combos:
        for reflector in REFLECTORS:
            run_auto_bombe.run(
                plain_crib,
                cipher_crib,
                top_rotor,
                middle_rotor,
                bottom_rotor,
                starting_letters,
                reflector,
                False,
                True
            )

    print('That took {} seconds'.format(time.time() - starttime))
