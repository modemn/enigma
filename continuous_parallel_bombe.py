from menu_generator_1 import MenuGenerator
from bombe_2 import Bombe
import multiprocessing
import sys
import time

ROTORS = ['I', 'II', 'III', 'IV', 'V']
REFLECTORS = ['A', 'B', 'C']


def run_bombe(
    plain_crib,
    cipher_crib,
    top_rotor,
    middle_rotor,
    bottom_rotor,
    starting_letters,
    reflector,
    settings,
    connections,
    input_letter,
    printing,
    output,
    q
):

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

    res = b.auto_run(plain_crib, cipher_crib)

    q.put(res)


if __name__ == '__main__':
    plain_crib = sys.argv[1].upper()
    cipher_crib = sys.argv[2].upper()
    starting_letters = sys.argv[3].upper()

    starttime = time.time()
    processes = []
    q = multiprocessing.Queue()
    rets = []

    mg = MenuGenerator(plain_crib, cipher_crib, starting_letters)
    settings, connections, input_letter, _ = mg.get_bombe_settings()

    rotor_combos = [
        (x, y, z) for x in ROTORS for y in ROTORS for z in ROTORS if x != y if y != z if x != z]

    for top_rotor, middle_rotor, bottom_rotor in rotor_combos:
        for reflector in REFLECTORS:
            p = multiprocessing.Process(target=run_bombe, args=(
                plain_crib,
                cipher_crib,
                top_rotor,
                middle_rotor,
                bottom_rotor,
                starting_letters,
                reflector,
                settings,
                connections,
                input_letter,
                False,
                False,
                q
            ))
            processes.append(p)
            p.start()

    for process in processes:
        ret = q.get()
        rets.append(ret)

    for process in processes:
        process.join()

    print('That took {} seconds'.format(time.time() - starttime))
    result = []
    list(map(result.extend, rets))
    print(result)
