import networkx as nx
import matplotlib.pyplot as plt

ALPHABET = 'ABCDEFGHIJKLMNOPQRSTUVWXYZ'


class MenuGenerator:
    def __init__(self, plain_crib, cipher_crib, starting_letters):
        top_idx = ALPHABET.find(starting_letters[0])
        middle_idx = ALPHABET.find(starting_letters[1])
        bottom_idx = ALPHABET.find(starting_letters[2])

        letters = plain_crib+cipher_crib

        menu = nx.Graph()

        menu.add_nodes_from(letters)

        connections = tuple(zip(plain_crib, cipher_crib))

        edge_labels = {}
        for i in range(len(connections)):
            bottom_idx = (bottom_idx + 1) % 26
            if (bottom_idx == ALPHABET.find(starting_letters[2])):
                middle_idx = (middle_idx + 1) % 26
                if (middle_idx == ALPHABET.find(starting_letters[1])):
                    top_idx = (top_idx + 1) % 26

            label = ALPHABET[top_idx]+ALPHABET[middle_idx]+ALPHABET[bottom_idx]

            edge_labels[connections[i]] = label

        menu.add_edges_from(connections)

        pos = nx.planar_layout(menu)

        plt.figure()

        nx.draw(menu, pos, edge_color='black', width=1, linewidths=1,
                node_size=200, node_color='red', alpha=0.9,
                labels={node: node for node in menu.nodes()})

        nx.draw_networkx_edge_labels(
            menu, pos, edge_labels=edge_labels, font_color='black')

        plt.axis('off')
        plt.show()


print('Plain crib:')
plain_crib = input().replace(" ", "").upper()

print('Cipher crib:')
cipher_crib = input().replace(" ", "").upper()

print('Starting letters:')
starting_letters = input().replace(" ", "").upper()

assert len(starting_letters) == 3, 'There should be 3 starting letters!'
assert len(plain_crib) == len(
    cipher_crib), 'The cipher and plain cribs should be of the same length'

mg = MenuGenerator(plain_crib, cipher_crib, starting_letters)
