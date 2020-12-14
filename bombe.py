from enigma import Enigma
from indicator import Indicator
from pprint import pprint

ALPHABET = 'ABCDEFGHIJKLMNOPQRSTUVWXYZ'


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

            # Reset all steckers
            for letter in ALPHABET:
                self.steckers[letter] = ''

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
                if not (len(set(path_string)) == len(path_string)):
                    closures.append(path_string)

            all_consistent_letters = []

            # Iterate through the closures
            valid_stop = True
            for closure in closures:
                consistent_letters = []

                # Find all letters that stay the same after going through all the scramblers
                for i in range(26):
                    if(ALPHABET[i] == dfs_tree_paths[closure][-1][i]):
                        consistent_letters.append(ALPHABET[i])

                # If there are no consistent letters or there are multiple, then invalid stop
                if (len(consistent_letters) != 1):
                    print(consistent_letters,
                          '<- multiple/no consistent letters, invalid stop!')
                    valid_stop = False
                    break
                # # Or if there are multiple different consistent letters, then invalid stop
                # elif (len(set(consistent_letters) != 1)):
                #     valid_stop = False
                #     break
                # Otherwise, generate and add to the potential steckers
                else:
                    all_consistent_letters.append(consistent_letters)
                    self.generate_steckers(
                        closure, dfs_tree_paths[closure], consistent_letters[0])

            # If the steckers are consistent and there was only 1 consistent letter per closure
            if (self.check_steckers(self.steckers) and valid_stop):
                print('Outputs through closures:')
                for closure in closures:
                    pprint(dfs_tree_paths[closure])
                    print()
                print('Consistent letters:', all_consistent_letters)
                print()
                print('Possible steckers:')
                self.print_steckers()
                print()
                print('Possible ring settings:')
                self.print_ring_settings()
                input()

            # Step scramblers
            for scrambler in self.scramblers:
                scrambler.step_rotors(True)

            # Step indicator
            self.indicator.step_rotors()

            iteration += 1

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
                    print(i, 'steckered to two letters, contradiction!')
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
            if ((len(self.steckers[s]) > 0) and (s != self.steckers[s]) and (s not in to_print)):
                to_print += s+self.steckers[s]+' '
        print(to_print)

    def print_ring_settings(self):
        to_print = ''
        to_print += self.indicator.t_rotor.current_letter()+' '
        to_print += self.indicator.m_rotor.current_letter()+' '
        to_print += self.indicator.b_rotor.current_letter()+' - '
        to_print += str(ALPHABET.find(self.indicator.t_rotor.current_letter())+1)+' '
        to_print += str(ALPHABET.find(self.indicator.m_rotor.current_letter())+1)+' '
        to_print += str(ALPHABET.find(self.indicator.b_rotor.current_letter())+1)
        print(to_print)


# Reflector: B
# Wheels: II-V-III
# Crib: WETTERVORHERSAGE
# Cipher crib: SNMKGGSTZZUGARLV
# b = Bombe(
#     'II',  # TOP / LEFT ROTOR
#     'V',  # MIDDLE ROTOR
#     'III',  # BOTTOM / RIGHT ROTOR
#     'ZZZ',
#     'B',  # REFLECTOR
#     ['ZZK', 'ZZE', 'ZZF', 'ZZN', 'ZZM', 'ZZG',
#         'ZZP', 'ZZB', 'ZZJ', 'ZZI', 'ZZL', 'ZZO'],  # SCRAMBLER SETTINGS
#     ['UE', 'EG', 'GR', 'RA', 'AS', 'SV', 'VE', 'EN',
#         'HZ', 'ZR', 'RG', 'GL'],  # CONNECTIONS
#     'E'  # INPUT LETTER
# )

# Reflector: B
# Wheels: III-II-V
# Start: M F I
# Rings: 07 20 05 (G T E)
# Plugged: JA NG LW CU ED BH QM VF ZK
# Crib: VELITESSECILLUMDOLORE
# Cipher crib:
# b = Bombe(
#     'III',  # TOP / LEFT ROTOR
#     'II',  # MIDDLE ROTOR
#     'V',  # BOTTOM / RIGHT ROTOR
#     'ZZZ',
#     'B',  # REFLECTOR
#     ['ZZF', 'ZZD', 'ZZJ', 'ZZC', 'ZZR', 'ZZO', 'ZZI',
#         'ZZU', 'ZZK', 'ZZT', 'ZZA'],  # SCRAMBLER SETTINGS
#     ['EI',  'IC',  'CX',  'XL',  'LM',  'MO',  'OE',
#         'EX',  'IK',  'KR',  'EV'],  # CONNECTIONS
#     'E'  # INPUT LETTER
# )

# Reflector: B
# Wheels: III - II - V
# Start: U C R
# Rings: 14 09 20
# Plugged: LS VY MT EW QG DX JZ IP FC BU
# Crib: ANATTACKONDURHAMAT
# Cipher crib:  ZPJABYGHRHGYZJILRJ
# b = Bombe(
#     'III',  # TOP / LEFT ROTOR
#     'II',  # MIDDLE ROTOR
#     'V',  # BOTTOM / RIGHT ROTOR
#     'ZZZ',
#     'B',  # REFLECTOR
#     ['ZZA', 'ZZM', 'ZZQ', 'ZZD', 'ZZR', 'ZZC', 'ZZI', 'ZZE',
#         'ZZF', 'ZZL', 'ZZO', 'ZZN'],  # SCRAMBLER SETTINGS
#     ['AZ',  'ZR',  'RA',  'AT',  'TJ',  'JA',  'RO',
#         'TB',  'AY',  'YU',  'AI',  'JH'],  # CONNECTIONS
#     'A'  # INPUT LETTER
# )


# Reflector: B
# Wheels: III - II - V
# Start: M F I
# Rings: 07 20 05
# Plugged: JA NG LW CU ED BH QM VF ZK
# Crib: LOREMIPSUMDOLORSITAMETCONSECTETUR
# Cipher crib:  DZPLBKWVJKQMRHXYYIKIVWMEBRYDNSKLQ
b = Bombe(
    'III',  # TOP / LEFT ROTOR
    'II',  # MIDDLE ROTOR
    'V',  # BOTTOM / RIGHT ROTOR
    'ZZZ',
    'B',  # REFLECTOR
    ['ZZR', 'ZZQ', 'ZZP', 'ZAZ', 'ZZC', 'ZZG', 'ZZV', 'ZAC',
        'ZZY', 'ZZE', 'ZZT', 'ZZR'],  # SCRAMBLER SETTINGS
    ['TI',  'IY',  'YS',  'SR',  'RP',  'PW',  'WT',
        'TN',  'NB',  'BM',  'MI',  'IT'],  # CONNECTIONS
    'T'  # INPUT LETTER
)

b.run()
