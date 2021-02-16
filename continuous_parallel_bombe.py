import sys
import time
from multiprocessing import Process
import run_auto_bombe

ROTORS = ['I', 'II', 'III', 'IV', 'V']
REFLECTORS = ['A', 'B', 'C']

plain_crib = sys.argv[1].upper()
cipher_crib = sys.argv[2].upper()
reflector = sys.argv[3].upper()
starting_letters = sys.argv[4].upper()


if __name__ == '__main__':
    starttime = time.time()
    processes = []
    rotor_combos = [
        (x, y, z) for x in ROTORS for y in ROTORS for z in ROTORS if x != y if y != z if x != z]
    for top_rotor, middle_rotor, bottom_rotor in rotor_combos:
        for reflector in REFLECTORS:
            p = Process(target=run_auto_bombe.run, args=(
                plain_crib,
                cipher_crib,
                top_rotor,
                middle_rotor,
                bottom_rotor,
                starting_letters,
                reflector,
                False,
                False
            ))
            processes.append(p)
            p.start()

    for process in processes:
        process.join()

    print('That took {} seconds'.format(time.time() - starttime))
