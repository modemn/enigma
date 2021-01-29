import networkx as nx
import matplotlib.pyplot as plt
import math
import random
from pprint import pprint

ALPHABET = 'ABCDEFGHIJKLMNOPQRSTUVWXYZ'


class MenuGenerator:
    def __init__(self, plain_crib, cipher_crib, starting_letters):
        self.scrambler_settings = []
        self.scrambler_connections = []
        top_idx = ALPHABET.find(starting_letters[0])
        middle_idx = ALPHABET.find(starting_letters[1])
        bottom_idx = ALPHABET.find(starting_letters[2])

        letters = plain_crib+cipher_crib

        self.menu = nx.Graph()

        self.menu.add_nodes_from(letters)

        connections = tuple(zip(plain_crib, cipher_crib))

        self.edge_labels = {}
        for i in range(len(connections)):
            bottom_idx = (bottom_idx + 1) % 26
            if (bottom_idx == ALPHABET.find(starting_letters[2])):
                middle_idx = (middle_idx + 1) % 26
                if (middle_idx == ALPHABET.find(starting_letters[1])):
                    top_idx = (top_idx + 1) % 26

            label = ALPHABET[top_idx]+ALPHABET[middle_idx]+ALPHABET[bottom_idx]

            self.edge_labels[connections[i]] = label

        self.menu.add_edges_from(connections)

    def draw_menu(self):
        pos = nx.planar_layout(self.menu)

        plt.figure()

        nx.draw(self.menu, pos, edge_color='black', width=1, linewidths=1,
                node_size=200, node_color='red', alpha=0.9,
                labels={node: node for node in self.menu.nodes()})

        nx.draw_networkx_edge_labels(
            self.menu, pos, edge_labels=self.edge_labels, font_color='black')

        plt.axis('off')
        plt.show()

    def get_closures(self, graph):
        closures = []
        g = nx.DiGraph(graph)

        res = list(nx.simple_cycles(g))

        for cl in res:
            if len(cl) > 2:
                if (set(''.join(cl)) not in [set(x) for x in closures]):
                    closures.append(''.join(cl))

        return closures

    def shortest_path_between_closures(self, closure_1, closure_2):
        shortest_path = None
        shortest_path_length = math.inf

        for u in closure_1:
            for v in closure_2:
                path = nx.shortest_path(G=self.menu, source=u, target=v)
                if (len(path) < shortest_path_length):
                    shortest_path_length = len(path)
                    shortest_path = path

        return shortest_path, shortest_path_length

    def add_settings(self, path):
        for i in range(len(path)):
            if i != len(path)-1:
                connection = path[i:i+2]
                try:
                    setting = self.edge_labels[tuple(
                        [connection[0], connection[1]])]
                except:
                    setting = self.edge_labels[tuple(
                        [connection[1], connection[0]])]

                self.scrambler_settings.append(setting)
                self.scrambler_connections.append(connection)

    def get_bombe_settings(self):

        # Find all the closures in the menu
        closures = self.get_closures(self.menu)
        closures.sort(key=len)
        closures = [x for x in closures if len(x) <= 11]
        closures.reverse()

        self.add_settings(closures[0]+closures[0][0])

        # Check for and remove disconnected closures if there are more than one closures
        if (len(closures) > 1):
            # Initialise dictionary
            connected_closures = {}
            for cl in closures:
                connected_closures[cl] = []
            # Iterate through the closures
            for i in range(len(closures)):
                # Check for a path to all other closures
                for j in range(i+1, len(closures)):
                    # If there is a path, save it in the dictionary
                    if (nx.has_path(self.menu, closures[i][0], closures[j][0])):
                        connected_closures[closures[i]].append(closures[j])
                        connected_closures[closures[j]].append(closures[i])

            # Keep only the connected closures ie keys in the dictionary with a non-zero length value
            closures = [v[0] for v in connected_closures.items() if len(v[1])]

            # Iterate through the closures connected to the first closure
            for neighbour in connected_closures[closures[0]]:
                # Find shortest path to the neighbouring clousre
                path, path_len = self.shortest_path_between_closures(
                    closures[0], neighbour)

                # If adding the path to the clousre and all its edges to the
                # connections doesn't go over our limit of 12, then add it
                if (len(self.scrambler_connections) + len(neighbour) + path_len < 12):
                    self.add_settings(''.join(path))
                    self.add_settings(neighbour+neighbour[0])

        # If there is still space for more scramblers then add on tails
        while (len(self.scrambler_connections) < 12):
            added = False
            while not added:
                settings_nodes = list(set(''.join(self.scrambler_connections)))
                node = random.choice(settings_nodes)
                for neighbour in self.menu[node]:
                    edge = str(node+neighbour)
                    try:
                        edge_label = self.edge_labels[tuple(edge)]
                    except:
                        edge_label = self.edge_labels[tuple(edge[::-1])]
                    if (edge_label not in self.scrambler_settings):
                        self.add_settings(edge)
                        added = True

        return self.scrambler_settings, self.scrambler_connections


# print('Plain crib:')
# plain_crib = input().replace(" ", "").upper()
# plain_crib = 'WETTERVORHERSAGE'
plain_crib = 'TAETIGKEITSBERIQTVOM'

# print('Cipher crib:')
# cipher_crib = input().replace(" ", "").upper()
# cipher_crib = 'SNMKGGSTZZUGARLV'
cipher_crib = 'YMZAXOZBCWGZFIGIMWXQ'

# print('Starting letters:')
# starting_letters = input().replace(" ", "").upper()
starting_letters = 'ZZZ'

assert len(starting_letters) == 3, 'There should be 3 starting letters!'
assert len(plain_crib) == len(
    cipher_crib), 'The cipher and plain cribs should be of the same length'

mg = MenuGenerator(plain_crib, cipher_crib, starting_letters)
settings, connections = mg.get_bombe_settings()
pprint(list(zip(settings, connections)))
mg.draw_menu()
