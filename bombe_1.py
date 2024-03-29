from os import altsep
from enigma import Enigma
from indicator import Indicator
from pprint import pprint
import time

ALPHABET = 'ABCDEFGHIJKLMNOPQRSTUVWXYZ'


class TimerError(Exception):
    """A custom exception used to report errors in use of Timer class"""


class Timer:
    def __init__(self):
        self._start_time = None
        self.elapsed_time = 0

    def start(self):
        """Start a new timer"""
        self._start_time = time.perf_counter()

    def stop(self):
        """Stop the timer, and report the elapsed time"""
        if self._start_time is None:
            raise TimerError(f"Timer is not running. Use .start() to start it")

        elapsed_time = time.perf_counter() - self._start_time
        self.elapsed_time += elapsed_time
        print(f"Elapsed time: {self.elapsed_time:0.4f} seconds")


class Bombe():
    """ A Bombe Machine

    Creates a Bombe machine with specified rotors and settings from a menu. Using this input, a graph is made and the alphabet travserses through it in a DFS fashion. When a loop is detected, the output alphabet is checked to see if any letter has not changed, this indicates a possible consistent set of letter steckerings. The steckers are checked for consistency, and if they are found to be valid, they are saved to a full steckering.

    Args:
        t_rotor (str): This is the name of the top rotor (represents the leftmost rotor on the enigma) ['I', 'II', 'III', 'IV', 'V'].
        m_rotor (str): This is the name of the middle rotor ['I', 'II', 'III', 'IV', 'V'].
        b_rotor (str): This is the name of the bottom rotor (represents the rightmost rotor on the enigma) ['I', 'II', 'III', 'IV', 'V'].
        indicator (str): This is the letters for the indicator drum to start with. Top rotor is the first letter and so on.
        reflector (str): This is the name of the reflector from ['A', 'B', 'C'].
        scrambler_settings (list(str)): This is a list of letters representing the starting letters of each scrambler in order.
        connections (list(str)): This is a list of the letters connected to each other. Each scrambler represents a letter. This order matches the list of scramblers.
        input (str): This is the input letters used as the source node of the DFS.

    Attributes:
        input (str): This is the input letters used as the source node of the DFS.
        scramblers (list(Scrambler)): This is a list of scramblers using the Enigma class set with the settings given in the arguments.
        indicator (Indicator): This is an Indicator which shows the possible ring settings at each stop.
        steckers (dict): This is a dictionary of each letter mapped to the possible steckered letter
        menu (dict): This is the menu graph generated from the input arguments. Keys are letters which represent nodes, values are lists of letters representing edges between nodes. Edges are between letters given as connections in the argument.

    Methods:
        run(): Runs the Bombe machine, printing out stops as and when they are found

        generate_steckers(path, outputs):
            Generates a steckering dictionary given the path and list of outputs
            Args:
                path (str): Letters representing which nodes the alphabet has traversed through
                outputs (list(str)): The output from each scrambler the alphabet has traversed through

        check_steckers(steckers):
            Checks the conisitency of a given steckering
            Args:
                steckers (dict): A dictionary of each letter mapped to the possible steckered letter.
            Returns:
                (bool): Whether the steckers given were consistent or not

        dfs(v, parent, visited, path, dfs_tree_paths, to_scramble):
            A recursive function to traverse the menu and push the alphabet through each eage
            Args:
                v (str): The current node in the traversal
                visited (list(bool)): List of booleans, ith bool represents the ith node visited status.
                path (str): A string of letters representing the path traversed prior to arriving at the current node, v.
                dfs_tree_paths (dict): A dictionary holding all paths and a list of the outputs after each traversal of that path.
                to_scramble (str): The string of letters to input into the next edge to receive the output scrambled output. This starts of as the usual alphabet.

        scramble(starting_letters, input):
            Scrambles the given input through the scramblers whose starting letters are the ones given.
            Args:
                starting_letters (str): The letters given as the starting letters of the scrmabler that the input should be scrambled through
                input (str): The string to scrambler through the given scrambler
            Returns:
                (str): The output of the scrambler.

        print_steckers():
            Prints the steckers with pairs of letters being plugged and spaces between each pair

        print_ring_settings():
            Prints the ring settings as number poisitions and letters

    """

    def __init__(self, t_rotor, m_rotor, b_rotor, indicator, reflector, scrambler_settings, connections, input):
        # Store rotors for outputting at a stop
        self.l_rotor = t_rotor
        self.m_rotor = m_rotor
        self.r_rotor = b_rotor

        # Calculate what the starting letter should really be for outputting at a stop
        self.starting_letters = ''
        for letter in indicator:
            self.starting_letters += ALPHABET[ALPHABET.find(letter)-1]

        # Initialize the input letter to DFS with as the source node
        self.input = input

        # Initialize scramblers
        self.scramblers = []
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

        # Initialize indicator scrambler
        self.indicator = Indicator([indicator[0], indicator[1], indicator[2]])

        # Initialize possible stecker dictionary
        self.steckers = {}
        for letter in ALPHABET:
            self.steckers[letter] = ''

        # Initialize the menu graph
        self.menu = {}
        all_connections = ''
        for connection in connections:
            all_connections += connection

        # Get all the menu nodes from the unique letters in all the connections
        nodes = "".join(set(all_connections))
        for node in nodes:
            self.menu[node] = []

        # Construct the menu
        for i in range(len(connections)):

            # Create the forward and backward edge tuples, both edges
            # to make the menu undirected
            # The first item in the tuple is this node's neighbour
            # The second item in the tuple is the scrambler's starting letters
            # associated with that connection (edge labels)
            forward_edge = (connections[i][1], scrambler_settings[i])
            backward_edge = (connections[i][0], scrambler_settings[i])

            # Add both edges to the menu if it doesn't already exist
            if forward_edge not in self.menu[connections[i][0]]:
                self.menu[connections[i][0]].append(forward_edge)

            if backward_edge not in self.menu[connections[i][1]]:
                self.menu[connections[i][1]].append(backward_edge)

        # pprint(self.menu)

    def run(self):
        timer = Timer()
        timer.start()
        stop = False
        iteration = 0

        # While we are not done going through the search space
        # and a stop hasn't occurred
        while ((iteration < 17576) and (not stop)):

            top_row = ''
            middle_row = ''
            bottom_row = ''

            for scrambler in self.scramblers:
                top_row += str(scrambler.l_rotor.current_letter_setting())
                middle_row += str(scrambler.m_rotor.current_letter_setting())
                bottom_row += str(scrambler.r_rotor.current_letter_setting())

            top_row += ' '+str(self.indicator.t_rotor.current_letter())
            middle_row += ' '+str(self.indicator.m_rotor.current_letter())
            bottom_row += ' '+str(self.indicator.b_rotor.current_letter())

            print(iteration, '----------------------------------')
            print('Scrambler settings:')
            print(top_row)
            print(middle_row)
            print(bottom_row)
            print()

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
                # TODO: I can change the line below to if (len(set(path_string)) != len(path_string)):
                if not (len(set(path_string)) == len(path_string)):
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
                        timer.stop()
                        print(
                            '######################## STOP ########################')

                        print('Outputs through closures:')
                        for closure in closures:
                            pprint(dfs_tree_paths[closure])
                            print()
                        print('Consistent letters:', consistent_letters)
                        print()

                        print()
                        print('Rotors:', self.l_rotor,
                              self.m_rotor, self.r_rotor)
                        print()
                        print('Starting letters:', self.starting_letters)
                        print()
                        print('Possible steckers:', self.print_steckers())
                        print()
                        print('Possible ring settings:',
                              self.print_ring_settings())
                        print()
                        print(
                            '######################## STOP ########################')
                        input()
                        timer.start()

            # Step scramblers
            for scrambler in self.scramblers:
                scrambler.step_rotors(True)

            # Step indicator
            self.indicator.step_rotors()

            iteration += 1

        timer.stop()

    # Function that geneates steckers and checks if they are consistent
    def generate_steckers(self, path, outputs, consistent_letter):
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

    def check_steckers(self, steckers):
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

    # Recursive function that creates tree paths using DFS
    def dfs(self, v, parent, visited, path, dfs_tree_paths, to_scramble):

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
    def scramble(self, starting_letters, input):
        # Find the index of the scrambler whose starting letters are the ones given
        scrambler_idx = [''.join(x.starting_letters) for x in self.scramblers].index(
            starting_letters)

        # Return the output of scrambling the input through the scrambler
        return self.scramblers[scrambler_idx].encrypt(input)

    def print_steckers(self):
        to_print = ''
        for s in self.steckers.keys():
            if ((len(self.steckers[s]) > 0) and (s not in to_print)):
                to_print += s+self.steckers[s]+' '
        return to_print

    def print_ring_settings(self):
        to_print = ''
        to_print += self.indicator.t_rotor.current_letter()+' '
        to_print += self.indicator.m_rotor.current_letter()+' '
        to_print += self.indicator.b_rotor.current_letter()+' - '
        to_print += str(ALPHABET.find(self.indicator.t_rotor.current_letter())+1)+' '
        to_print += str(ALPHABET.find(self.indicator.m_rotor.current_letter())+1)+' '
        to_print += str(ALPHABET.find(self.indicator.b_rotor.current_letter())+1)
        return to_print


b = Bombe(
    'I',  # TOP / LEFT ROTOR
    'III',  # MIDDLE ROTOR
    'IV',  # BOTTOM / RIGHT ROTOR
    'ZZZ',
    'B',  # REFLECTOR
    ['ZZP', 'ZZN', 'ZZL', 'ZZF', 'ZZE', 'ZZK', 'ZZA', 'ZZI',
        'ZZC', 'ZZD', 'ZZG', 'ZZB'],  # SCRAMBLER SETTINGS
    ['EA',  'AL',  'LR',  'RI',  'IE',  'EH',  'HW',
        'RQ',  'QT',  'TR',  'LV',  'EX'],  # CONNECTIONS
    'E'  # INPUT LETTER
)

b.run()
