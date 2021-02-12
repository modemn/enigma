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

        return closures, len(closures)

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

        comps = nx.connected_components(self.menu)
        component_graphs = {}
        for comp in comps:
            closure_info = self.get_closures((self.menu.subgraph(comp)))
            if closure_info[1] > 0:
                component_graphs[tuple(comp)] = (
                    # Number of closures in the subgraph
                    closure_info[1],
                    # Total number of edges in the closures
                    sum([len(x) for x in closure_info[0]]),
                    # Nodes in the closures
                    closure_info[0]
                )

        if len(component_graphs) > 0:

            new_menu = nx.Graph()

            while len(component_graphs) > 0:
                # Find the component with the most closures,
                # tie break with component which has most closure edges
                max_comp = max(component_graphs, key=component_graphs.get)

                # Add the max component to the new_menu only if it has at least one closure,
                # max component could have no closures if the crib pair menu gives no clousres at all
                if component_graphs[max_comp][0] > 0:
                    new_menu = self.menu.subgraph(max_comp)
                    break
                else:
                    component_graphs.popitem(max_comp)

            closures = component_graphs[max(
                component_graphs, key=component_graphs.get)][2]
            closures.sort(key=len)
            # Remove closures with more than 12 edges
            closures = [x for x in closures if len(x) <= 12]
            closures.reverse()
            num_closures = 0

            # Always add the largest closure
            self.add_settings(closures[0]+closures[0][0])
            num_closures += 1

            # Add any other closures to the settings
            for cl in closures[1:]:
                # Find shortest path to the next largest closure
                path, path_len = self.shortest_path_between_closures(
                    closures[0], cl)

                # If adding the path to the closure and all its edges to connections doesn't go over our limit of 12, then add it
                if (len(self.scrambler_connections) + len(cl) + path_len < 12):
                    self.add_settings(''.join(path))
                    self.add_settings(cl+cl[0])
                    num_closures += 1

            # print(self.scrambler_settings, self.scrambler_connections)

            # Collect the edges available to be added to the settings
            available_edges = nx.Graph(new_menu)
            available_edges.remove_edges_from(self.scrambler_connections)
            # Remove nodes that have no edges, leaving endpoint nodes to available edges only
            available_edges.remove_nodes_from(
                list(nx.isolates(available_edges)))

            # If there is still space for more scramblers and there are edges availble to add then add on tails
            while (available_edges.size() > 0 and len(self.scrambler_connections) < 12):

                available_nodes = [x for x in available_edges.nodes if x in list(
                    set(''.join(self.scrambler_connections)))]

                # print(available_edges.nodes)
                # print(available_nodes)
                # input()

                # Pick a random node from the endpoints of available edges and a random neighbour as the edge
                node = random.choice(list(available_nodes))
                neighbour = random.choice(list(available_edges[node]))
                edge = str(node+neighbour)

                # Add the edge to the settings
                self.add_settings(edge)

                # Remove the edge from available edges
                available_edges.remove_edges_from([edge])
                available_edges.remove_nodes_from(
                    list(nx.isolates(available_edges)))

            # Find the input letter as the one with the highest degree in our menu
            joined_connections = ''.join(self.scrambler_connections)
            settings_degrees = dict((x, joined_connections.count(x))
                                    for x in set(joined_connections))
            input_letter = max(settings_degrees, key=settings_degrees.get)

            return self.scrambler_settings, self.scrambler_connections, input_letter, num_closures
        else:
            return [], [], '!', -1


# kina jr
# print('Plain crib:')
# plain_crib = input().replace(" ", "").upper()
plain_crib = 'WETTERVORHERSAGE'
# plain_crib = 'WETTERVORHERSAG'
# plain_crib = 'TAETIGKEITSBERIQTVOM'
# plain_crib = 'ORSITAMETC'
# 111111111111111111111111111111111111111111111
# plain_crib = 'ABCDADEGFHHI'

# print('Cipher crib:')
# cipher_crib = input().replace(" ", "").upper()
cipher_crib = 'SNMKGGSTZZUGARLV'
# cipher_crib = 'SNMKGGSTZZUGARL'
# cipher_crib = 'YMZAXOZBCWGZFIGIMWXQ'
# cipher_crib = 'YITCWTUWRT'
# 111111111111111111111111111111111111111111111
# cipher_crib = 'BCDBEFGFHIJJ'

# print('Starting letters:')
# starting_letters = input().replace(" ", "").upper()
starting_letters = 'ZZZ'

# assert len(starting_letters) == 3, 'There should be 3 starting letters!'
# assert len(plain_crib) == len(
#     cipher_crib), 'The cipher and plain cribs should be of the same length'

# mg = MenuGenerator(plain_crib, cipher_crib, starting_letters)
# pprint(mg.get_bombe_settings())
# mg.draw_menu()
