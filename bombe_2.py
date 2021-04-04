from enigma import Enigma
from indicator import Indicator
from timer import Timer

ALPHABET = 'ABCDEFGHIJKLMNOPQRSTUVWXYZ'


class Bombe():
    """ A class to represent a Turing Bombe machine.

    Attributes
    ----------
    l_rotor: str
        The top / leftmost rotor name.
    m_rotor: str
        The middle rotor name.
    r_rotor: str
        The bottom / rightmost rotor name.
    reflector: str
        The reflector name.
    starting_letters: str
        The letters the Enigma will start on. Leftmost rotor's letter specified first.
    input: str
        Letter to start the DFS process on.
    scramblers: list[Enigma]
        The scramblers.
    indicator: Indicator
        The indicator.
    steckers: dict[str, str]
        A dictionary of which letters are plugged to each other.
    menu: dict[str, list[tuple[str, str]]]
        The menu. The keys are node names, values are a list of tuples. The first item in the tuple is the node's neighbour. The second item in the tuple is the scrambler's starting letters associated with that connection.
    num_stops: int
        The number of stops.
    printing: bool
        Determines whether to print the scrambling steps to the terminal.
    output: bool
        Deteremines whether to output to a file names 'bombe_output.txt'.
    crib: tuple[str, str]
        The plain and cipher cribs.

    Methods
    -------
    run()
        Runs the bombe.
    auto_run(plain_crib, cipher_crib)
        Sets the crib tuple attribute and then runs the bombe.
    generate_steckers(path, outputs, consistent_letter)
        Generates the steckers given the outputs of each stage of the DFS process and the letter that stayed consistent.
    check_steckers(steckers)
        Checks to see if the steckers given are valid ie each key has one unique letter value.
    dfs(v, parent, visited, path, dfs_tree_paths, to_scramble)
        Traverses the menu and scrambles through each stage and saves the output.
    scramble(starting_letters, input_str)
        Scrambles the input through and Enigma with the starting letters provided.
    print_steckers()
        Prints the steckers.
    adjust_ring_start_letters()
        Adjusts the ring setting so that they are as far as possible from a middle rotor shift.
    """

    def __init__(
        self,
        t_rotor: str,
        m_rotor: str,
        b_rotor: str,
        indicator: str,
        reflector: str,
        scrambler_settings: list[str],
        connections: list[str],
        input_letter: str,
        printing: bool,
        output: bool
    ):
        """
        Parameters
        ----------
        t_rotor: str
            The top / leftmost rotor's name.
        m_rotor: str
            The middle rotor's name.
        b_rotor: str
            The bottom / rightmost rotor's name.
        indicator: str
            The letters to start the Inidicator with, translates to the ring settings that the Enigma will start with.
        reflector: str
            The reflector's name.
        scrambler_settings: list[str]
            The starting letters of each scrambler.
        connections: list[str]
            Pairs of letters representing which pairs of scramblers connect.
        input_letter: str
            The letter to start the DFS process on.
        printing: bool
            Determines whether to print the scrambling steps to the terminal.
        output: bool
            Deteremines whether to output to a file names 'bombe_output.txt'.
        """
        self.l_rotor = t_rotor
        self.m_rotor = m_rotor
        self.r_rotor = b_rotor
        self.reflector = reflector
        self.starting_letters: str = ''
        self.input = input_letter
        self.scramblers: list[Enigma] = []
        self.indicator = Indicator([indicator[0], indicator[1], indicator[2]])
        self.steckers: dict[str, str] = {}
        self.menu: dict[str, list[tuple[str, str]]] = {}
        self.num_stops: int = 0
        self.printing = printing
        self.output = output
        self.crib: tuple[str, str] = ()

        for letter in indicator:
            self.starting_letters += ALPHABET[ALPHABET.find(letter)-1]

        for i in range(len(scrambler_settings)):
            self.scramblers.append(
                Enigma(
                    False,
                    False,
                    False,
                    [str(t_rotor), str(m_rotor), str(b_rotor)],
                    list(scrambler_settings[i]),
                    ['1', '1', '1'],
                    reflector,
                    []
                )
            )
        for letter in ALPHABET:
            self.steckers[letter] = ''
        all_connections = ''

        for connection in connections:
            all_connections += connection
        nodes = "".join(set(all_connections))

        for node in nodes:
            self.menu[node] = []

        for i in range(len(connections)):
            forward_edge = (connections[i][1], scrambler_settings[i])
            backward_edge = (connections[i][0], scrambler_settings[i])

            if forward_edge not in self.menu[connections[i][0]]:
                self.menu[connections[i][0]].append(forward_edge)

            if backward_edge not in self.menu[connections[i][1]]:
                self.menu[connections[i][1]].append(backward_edge)

        if self.output:
            settings = list(zip(scrambler_settings, connections))
            with open('bombe_output.txt', 'w', newline='') as file:
                file.write(
                    f'Rotors: {self.l_rotor}, {self.m_rotor}, {self.r_rotor}\n')
                file.write(f'Reflector: {self.reflector}\n\n')
                file.write('Connections:\n')
                for s in settings:
                    file.write(f'{s}\n')
                file.write('\n')

    def run(self):
        """Runs the Bombe simulator.

        Tries to find stops given the scrambler settings and the menu. Prints each stop's information if printing is True and outputs them to a file called 'bombe_output.txt' if output is True.

        Parameters
        ----------
        None

        Returns
        -------
        stops: list[str]
            A list of strings each containing information of all the stops found.
        """
        timer = Timer()
        timer.start()
        iteration = 0
        stops = []

        # While we are not done going through the search space
        # and a stop hasn't occurred
        while ((iteration < 17576)):

            # Intialize dictionary keeping track of visited nodes
            visited = {}
            for i in list(self.menu.keys()):
                visited[i] = False

            # Initialize dictionary keeping track of the paths and their outputs
            dfs_tree_paths = {self.input: [ALPHABET]}

            # DFS with the input as the source node
            self.dfs(
                self.input,  # current node
                0,  # parent of this node, initialised to 0 since this is the source
                visited,  # visited list
                str(self.input),  # path so far, initialized to just the input
                dfs_tree_paths,  # dictionary of all paths and all outputs
                ALPHABET  # initial string to scramble
            )

            # Iterate through the paths and save the closures
            closures = []
            for path_string in dfs_tree_paths.keys():
                if (len(set(path_string)) != len(path_string)):
                    closures.append(path_string)

            valid_stop = True
            consistent_letters = []

            # Iterate through the closures
            for closure in closures:

                # Find all letters that stay the same after traversing the loop of scramblers
                for i in range(26):
                    if(ALPHABET[i] == dfs_tree_paths[closure][-1][i]):
                        consistent_letters.append(ALPHABET[i])

                # If there are no consistent letters, then invalid stop
                if (len(consistent_letters) < 1):
                    valid_stop = False
                    break

                # Check whether any of the consistent letters found give a valid steckering
                for cl in consistent_letters:
                    # Reset all steckers
                    for letter in ALPHABET:
                        self.steckers[letter] = ''

                    self.generate_steckers(
                        closure, dfs_tree_paths[closure], cl)

                    # Add the steckers deduced from non-closure paths
                    for path in dfs_tree_paths:
                        self.generate_steckers(path, dfs_tree_paths[path], cl)

                    # If the steckers are consistent and there was at least 1 consistent letter, then stop!
                    if (self.check_steckers(self.steckers) and valid_stop):
                        time = timer.stop()

                        adjusted_ring_settings, adjusted_starting_letters = self.adjust_ring_start_letters()

                        # If we got given a plain_crib then set up an enigma machine and encode with settings from the stop
                        if len(self.crib) > 0:

                            enigma_steckers = []
                            for s in self.steckers.keys():
                                if (len(self.steckers[s]) > 0 and (s not in ''.join(enigma_steckers)) and (s != self.steckers[s])):
                                    enigma_steckers.append(
                                        str(s+self.steckers[s]))

                            stop_enigma = Enigma(
                                False,
                                False,
                                True,
                                [self.l_rotor, self.m_rotor, self.r_rotor],
                                adjusted_starting_letters,
                                adjusted_ring_settings,
                                self.reflector,
                                enigma_steckers
                            )

                            stop_encryption = stop_enigma.encrypt(
                                self.crib[1])

                        if self.printing:
                            print(
                                '######################## STOP ########################')
                            print()
                            print(f'Time elapsed: {time:0.04f} seconds')
                            print('Rotors:', self.l_rotor,
                                  self.m_rotor, self.r_rotor)
                            print('Possible ring settings:',
                                  ' '.join(adjusted_ring_settings))
                            print('Starting letters:', ' '.join(
                                adjusted_starting_letters))
                            print('Possible steckers:', self.print_steckers())
                            print()
                            if len(self.crib[1]) > 0:
                                print(
                                    '~~~~~~~~~~~~~~~~~~~~ ENCRYPTION ~~~~~~~~~~~~~~~~~~~~')
                                print(f'{self.crib[1]} <- Cipher Crib')
                                print(f'{self.crib[0]} <- Plain crib')
                                print(
                                    f'{stop_encryption} <- Decrypted Cipher Crib with stop')
                                print()
                                print(
                                    '######################## STOP ########################')
                            else:
                                print(
                                    '######################## STOP ########################')
                            print()
                            timer.start()

                        if self.output:
                            self.num_stops += 1
                            with open('bombe_output.txt', 'a', newline='') as file:
                                file.write(f'STOP {str(self.num_stops)}\n')
                                file.write(f'Time: {time:0.4f}  seconds\n\n')
                                file.write(
                                    f'Possible Ring Settings: {" ".join(adjusted_ring_settings)}\n')
                                file.write(
                                    f'Starting Letters: {" ".join(adjusted_starting_letters)}\n')
                                file.write(
                                    f'Possible Steckers: {self.print_steckers()}\n\n')
                                if len(self.crib) > 0:
                                    file.write(
                                        f'{self.crib[1]} <- Cipher Crib\n')
                                    file.write(
                                        f'{self.crib[0]} <- Plain crib\n')
                                    file.write(
                                        f'{stop_encryption} <- Decrypted Cipher Crib with stop\n\n')
                            timer.start()

                        this_stop = f'Rotors: {self.scramblers[0].l_rotor.name} {self.scramblers[0].m_rotor.name} {self.scramblers[0].r_rotor.name}\nReflector: {self.reflector}\nPossible ring settings: {" ".join(adjusted_ring_settings)}\nStarting Letters: {" ".join(adjusted_starting_letters)}\nPossible Steckers: {self.print_steckers()}'

                        if len(self.crib) > 0:
                            this_stop += f'\n{self.crib[1]} <- Cipher Crib\n{self.crib[0]} <- Plain crib\n{stop_encryption} <- Decrypted Cipher Crib with stop'

                        stops += [this_stop]

            # Step scramblers
            for scrambler in self.scramblers:
                scrambler.step_rotors(True)

            # Step indicator
            self.indicator.step_rotors()

            iteration += 1

        end_time = timer.stop()

        if self.printing:
            print(f'End time: {end_time:0.4f}')

        if (self.output):
            with open('bombe_output.txt', 'a', newline='') as file:
                file.write(f'End time: {end_time:0.4f}\n')

        return stops

    def auto_run(self, plain_crib: str, cipher_crib: str):
        """Sets the plain and cipher crib attributes and then runs the Bombe simulator as usual.

        Parameters
        ----------
        plain_crib: str
            The plain crib.
        cipher_crib: str
            The cipher crib.

        Returns
        -------
        list[str]
            A list of strings each containing information of all the stops found.
        """
        self.crib = (plain_crib, cipher_crib)
        return self.run()

    def generate_steckers(self, path: str, outputs: list[str], consistent_letter: str):
        """Generates which letters are plugged to which others.

        Parameters
        ----------
        path: str
            The path of the closure the DFS process took to get this potential stop
        outputs: list[str]
            The outputs from each edge traversal in the DFS process.
        consistent_letter: str
            The letter that stayed the same after encrypting through the closure.

        Returns
        -------
        None
        """

        # Construct the steckering
        for i in range(len(outputs)):
            # Extract the steckering from the outputs
            self.steckers[path[i % len(self.scramblers)]
                          ] += outputs[i][ALPHABET.find(consistent_letter)]

            # Input the diagonal board connection too:
            # If A steckerd to B, then B is steckered to A
            self.steckers[outputs[i][ALPHABET.find(
                consistent_letter)]] += path[i % len(self.scramblers)]

    # Function that check if given steckers have no contradictions
    def check_steckers(self, steckers: dict[str, str]):
        """Checks if the given steckers have no contradictions.

        Parameters
        ----------
        steckers: dict[str, str]
            A dictionary of which letters are plugged to each other.

        Returns
        -------
        bool
            True if steckers are consistent ie each key has one unique value, otherwise False.
        """

        # Check if there are any steckers at all
        values = ''.join(steckers.values())
        if (len(steckers.keys()) and len(values)):

            # Iterate through the steckers
            for i in steckers.keys():

                # Remove any duplicate values from each steckering
                steckers[i] = ''.join(set(steckers[i]))

                # If the number of steckerings is still more than 1
                # then there must be a contradiction
                if (len(steckers[i]) > 1):
                    return False

            return True

        # If there are no steckers, then no consistent letters were found
        # so no need to save
        else:
            return False

    def dfs(
        self,
        v: str,
        parent: int,
        visited: dict[str, bool],
        path: str,
        dfs_tree_paths: dict[str, list[str]],
        to_scramble: str
    ):
        """Recursive function that creates tree paths using DFS.

        Parameters
        ----------
        v: str
            The current node in the DFS traversal.
        parent: int
            The current node's parent
        visited: dict[str, bool]
            A dictionary keeping track of which nodes have been visited.
        path: str
            The current path of traversal.
        dfs_tree_paths: dict[str, list[str]]
            A dictionary containing paths as keys and outputs from the paths as values.
        to_scramble: str
            The current string to scramble.


        Returns
        -------
        None
        """

        # Record that node v has been visited
        visited[v] = True

        # Iterate through the neigbhours of v
        for i in self.menu[v]:

            # If the node hasn't been visited before
            if not visited[i[0]]:

                # Extend the path with the neighbour i
                extended_path = path+str(i[0])

                # Scramble the input alphabet
                scrambler_output = self.scramble(i[1], to_scramble)

                # Append it on to the output alphabets from the path
                path_outputs = dfs_tree_paths[path] + [scrambler_output]

                # Insert it into the dictionary that holds all the paths
                # and their outputs
                dfs_tree_paths[extended_path] = path_outputs

                # Recurse with i as the source node and the extended path
                self.dfs(i[0], v, visited, extended_path,
                         dfs_tree_paths, scrambler_output)

            # If the node has been visited and it was not this
            # node's parent, then a loop is found, scramble one last time
            elif (visited[i[0]] and i[0] != parent):
                # print('Found a loop!')
                # Extend the path with the neighbour i
                extended_path = path+str(i[0])

                # Scramble the input alphabet
                scrambler_output = self.scramble(i[1], to_scramble)

                # Append it on to the output alphabets from the path
                path_outputs = dfs_tree_paths[path] + [scrambler_output]

                # Insert it into the dictionary that holds all the paths
                # and their outputs
                dfs_tree_paths[extended_path] = path_outputs

    # Function that returns the encryption of the input
    # through a scrambler whose starting letters are given
    def scramble(self, starting_letters: str, input_str: str):
        """Scrambles the input string

        Parameters
        ----------
        starting_letters: str
            Three letters denoting the starting letters of the scrambler rotors. Leftmost rotor's name specified first.
        input_str: str
            The string to scramble.


        Returns
        -------
        str
            The encrypted text.
        """

        # Find the index of the scrambler whose starting letters are the ones given
        scrambler_idx = [''.join(x.starting_letters) for x in self.scramblers].index(
            starting_letters)

        # Return the output of scrambling the input through the scrambler
        return self.scramblers[scrambler_idx].encrypt(input_str)

    def print_steckers(self):
        """Prints the steckers.

        Parameters
        ----------
        None

        Returns
        -------
        to_print: str
            The string to print the steckers nicely.

        """
        to_print = ''
        for s in self.steckers.keys():
            if ((len(self.steckers[s]) > 0) and (s not in to_print)):
                to_print += s+self.steckers[s]+' '
        return to_print

    def adjust_ring_start_letters(self):
        """Adjusts the ring settings of a stop so that the turnover point is as far from the beginning as possible.

        Paramaters
        ----------
        None

        Returns
        -------
        adjusted_ring_settings: list[str]
            The three ring settings the Enigma should be set up with for this stop. Leftmost rotor's setting is specified first.
        adjusted_starting_letters: list[str]
            The three starting letter the Enigma should be set up with for this stop. Leftmost rotor's starting letter is specified first.
        """

        r_ring = self.indicator.b_rotor.current_letter()

        # Find the position in the alphabet the right hand rotor's notch is located
        one_after_notch_index = (ALPHABET.index(
            self.scramblers[0].r_rotor.notch[0]) + 1) % 26

        # Step the right hand ring setting the same amount
        value = one_after_notch_index - \
            ALPHABET.index(self.starting_letters[2])
        r_ring_index = (ALPHABET.index(r_ring) + value) % 26

        # Set the right hand starting letter to this index
        adjusted_starting_letters = list(self.starting_letters)
        adjusted_starting_letters[2] = ALPHABET[one_after_notch_index]

        adjusted_ring_settings = [
            str(ALPHABET.find(self.indicator.t_rotor.current_letter())+1),
            str(ALPHABET.find(self.indicator.m_rotor.current_letter())+1),
            str(r_ring_index+1)
        ]

        return adjusted_ring_settings, adjusted_starting_letters
