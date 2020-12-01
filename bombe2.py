from enigma import Enigma
from indicator import Indicator
from pprint import pprint

ALPHABET = 'ABCDEFGHIJKLMNOPQRSTUVWXYZ'


class Bombe():
    def __init__(self, t_rotor, m_rotor, b_rotor, reflector, scrambler_settings, connections, input):
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
                    [str(b_rotor), str(m_rotor), str(t_rotor)],
                    list(scrambler_settings[i])[::-1],
                    ['1', '1', '1'],
                    reflector,
                    []
                )
            )

        # Initialize indicator scrambler
        self.indicator = Indicator(['Z', 'Z', 'Z'])

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
            # The first item in the tuple is the node this node is linked to
            # The second item in the tuple is the scrambler's starting letters
            # associated with that connection
            forward_edge = (connections[i][1], scrambler_settings[i])
            backward_edge = (connections[i][0], scrambler_settings[i])

            # Add the tuple to the menu if it doesn't already exist
            if forward_edge not in self.menu[connections[i][0]]:
                self.menu[connections[i][0]].append(forward_edge)

            if backward_edge not in self.menu[connections[i][1]]:
                self.menu[connections[i][1]].append(backward_edge)

        # pprint(self.menu)

    def run(self):
        stop = False
        iteration = 0

        # While we are not done going through the search space
        # and a stop hasn't occurred
        while ((iteration < 17576) and (not stop)):
            top_row = ''
            middle_row = ''
            bottom_row = ''

            for scrambler in self.scramblers:
                top_row += str(scrambler.r_rotor.current_letter_setting())
                middle_row += str(scrambler.m_rotor.current_letter_setting())
                bottom_row += str(scrambler.l_rotor.current_letter_setting())

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
            dfs_tree_paths = {
                self.input: [ALPHABET]
            }

            # Initialize list keeping track of all the possible steckers generated
            possible_steckers = []

            # DFS with the input as the source node
            # therefore the path is initialized to 's' for source
            self.dfs(self.input, 0, visited, str(
                self.input), dfs_tree_paths, ALPHABET)

            # Iterate through the paths to find ones with loops in them
            for path_string in dfs_tree_paths.keys():
                if not (len(set(path_string)) == len(path_string)):
                    # Generate the steckers associated with the looped path
                    steckers = self.generate_steckers(
                        path_string, dfs_tree_paths[path_string])

                    # And if the steckers are consistent, save them
                    if (self.check_steckers(steckers)):
                        possible_steckers.append(steckers)

            if (len(possible_steckers)):
                print('Possible steckers:')
                pprint(possible_steckers)
                print()
                print('Possible ring settings:')
                print(
                    self.indicator.t_rotor.current_letter(),
                    self.indicator.m_rotor.current_letter(),
                    self.indicator.b_rotor.current_letter()
                )
                input()

            # Step scramblers
            for scrambler in self.scramblers:
                scrambler.step_rotors(False)

            # Step indicator
            self.indicator.step_rotors()

            iteration += 1

    # Function that geneates steckers and checks if they are consistent
    def generate_steckers(self, path, outputs):
        # Check if there are any letters that don't change after
        # being scrambled through the loop
        consistent_letters = []
        for i in range(26):
            if(ALPHABET[i] == outputs[-1][i]):
                consistent_letters.append(ALPHABET[i])

        # Initialize possible steckers
        steckers = {}
        for letter in ALPHABET:
            steckers[letter] = ''

        # If there were consistent letters, then build
        # the steckering
        if (len(consistent_letters)):

            # Iterate through all the consistent letters
            for cl in consistent_letters:

                # Construct the steckering
                for i in range(len(outputs)):
                    # Extract the steckering from the outputs
                    steckers[path[i % len(self.scramblers)]
                             ] += outputs[i][ALPHABET.find(cl)]

                    # Input the diagonal board connection too:
                    # If A steckerd to B, then B is steckered to A
                    steckers[outputs[i][ALPHABET.find(
                        cl)]] += path[i % len(self.scramblers)]

        return steckers

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

                # Otherwise, check that the steckering is consistent
                else:
                    val = steckers[i]
                    if (val in steckers.keys()):
                        if (steckers[val] != i):
                            return False

            return True

        # If not, then no consistent letters were found
        # so no need to save
        else:
            return False

    # Recursive function that creates tree paths using DFS
    def dfs(self, v, parent, visited, path, dfs_tree_paths, to_scramble):
        # Record that node v has been visited
        visited[v] = True

        # Iterate through the neigbhours of v
        for i in self.menu[v]:

            # Extend the path with the current node v
            extended_path = path+str(i[0])

            # If the node hasn't been visited before
            if not visited[i[0]]:

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

            # If it has been visited before and it is not the parent
            # then a loop has been found
            elif (i[0] != parent):
                scrambler_output = self.scramble(i[1], to_scramble)
                path_outputs = dfs_tree_paths[path] + [scrambler_output]
                dfs_tree_paths[extended_path] = path_outputs

    # Function that returns the encryption of the input
    # through a scrambler whose starting letters are given
    def scramble(self, starting_letters, input):
        # Find the index of the scrambler whose starting letters are the ones given
        scrambler_idx = [x.starting_letters_for_bombe()
                         for x in self.scramblers].index(starting_letters)

        # Return the output of scrambling the input through the scrambler
        return self.scramblers[scrambler_idx].encrypt(input)


b = Bombe(
    'II',  # TOP / RIGHT ROTOR
    'V',  # MIDDLE ROTOR
    'III',  # BOTTOM / LEFT ROTOR
    'B',  # REFLECTOR
    ['ZZK', 'ZZE', 'ZZF', 'ZZN', 'ZZM', 'ZZG',
        'ZZP', 'ZZB', 'ZZJ', 'ZZI', 'ZZL', 'ZZO'],  # SCRAMBLER SETTINGS
    ['UE', 'EG', 'GR', 'RA', 'AS', 'SV', 'VE', 'EN',
        'HZ', 'ZR', 'RG', 'GL'],  # CONNECTIONS
    'E'  # INPUT LETTER
)

b.run()
