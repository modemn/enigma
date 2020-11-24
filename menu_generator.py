import networkx as nx
import matplotlib.pyplot as plt

# plain_crib = input()
# cipher_crib = input()

plain_crib = 'XANFANGSUEDAUSGANGBA'
cipher_crib = 'DXTGNVHVRMMEVOUYFZSL'

letters = plain_crib+cipher_crib
# letters = "".join(set(letters))

menu = nx.Graph()

menu.add_nodes_from(letters)

connections = tuple(zip(plain_crib, cipher_crib))

edge_labels = {}
for i in range(len(connections)):
    edge_labels[connections[i]] = str(i+1)

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
# plt.savefig('menu.png')

# nx.draw(menu, with_labels=True, font_weight='bold')
# plt.show()
