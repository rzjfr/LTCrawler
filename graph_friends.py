import books
import friends
import json
from HelperMethods import *
from networkx import *
import matplotlib.pyplot as plt
from networkx import graphviz_layout


def get_adjacancy_list(members):
    """(list)-> dict
    dsc: returns a list of friends and for given members
    """
    result = {}
    while members:
        members = list(set(members))
        name = members.pop()
        print len(members), name
        if name not in result:
            all_friends = friends.find_friends(name)
            result.update({name: all_friends})
            if all_friends.__class__ == list and all_friends:
                members.extend(all_friends)
    return result


def find_adjacancy_list(work):
    """(str)->dict
    dsc: loads all members of a work and save user name with all friends of her
    to a json file
    """
    file_path = './%s_members.json' % work
    try:  # if we have information alredy
        with open(file_path):
            adj_list = load_local_friends(file_path)
    except IOError:  # otherwise calc it and save it  for further use
        # Note: this algorithm is very ineficient thats why we save the result
        members = books.find_all_members(work)
        print len(members)
        print len(remove_duplicate(members))
        adj_list = get_adjacancy_list(members)
        print len(adj_list)
        for k, v in adj_list.items():
            record = json.dumps({k: v})
            write_to_file(record, file_path)
    return adj_list


def find_junk_nodes(adj_list, members):
    """(dict, list)->dict
    dsc: returns nodes that has no friend list
    """
    strings = ['No connection', 'No list', 'Private', 'NA', 'Not exist',
               'Removed', 'No access']
    junk_nodes = []
    for item in strings:
        junk_nodes.extend(find_key_by_value(item, adj_list))
    temp = []  # we dont want to ignore book members
    for item in junk_nodes:
        if item not in members:
            temp.append(item)
    junk_nodes = remove_duplicate(temp)
    return junk_nodes


def find_null_nodes(adj_list, members):
    """(dict, list)->dict
    dsc: returns nodes that has no friend list
    """
    null_nodes = []
    null_friends = find_null_friends(adj_list)
    for item in null_friends:
        if item not in members:
            null_nodes.append(item)
    null_nodes = remove_duplicate(null_nodes)
    return null_nodes


def clean_adj_list(adj_list, junk_nodes, null_nodes):
    """(dict, list, list)->dict
    dsc: returns cleaned adjacancy list
    """
    remove = junk_nodes + null_nodes  # all nodes we want to remove
    cleaned_adj_list = {}
    for name, friends in adj_list.items():
        print '%d item processed' % len(cleaned_adj_list)
        if name not in remove:
            cleaned_friends = []
            if friends.__class__ == list:
                for friend in friends:
                    if friend not in remove:
                        cleaned_friends.append(friend)
            cleaned_adj_list.update({name: cleaned_friends})
    return cleaned_adj_list


def make_cleand_adjacancy_list(adj_list):
    """(dict, str)->dict
    dsc: make clean adjacancy list from given adj_list
    >>>make_cleand_adjacancy_list({1: [2, 4, 5], 2: [1, 6, 7, 8, 9], 3: [4],
                                   4: 'No connection', 5: 'No list',
                                   6: 'Removed', 7: 'No connection', 8: []})
    {1: [2], 2: [1, 9]}
    """
    init_len = len(adj_list)

    junk_nodes = find_junk_nodes(adj_list, members)
    null_nodes = find_null_nodes(adj_list, members)
    adj_list = clean_adj_list(adj_list, junk_nodes, null_nodes)
    removed_len = len(junk_nodes) + len(null_nodes)

    # remove null records
    junk_nodes = find_junk_nodes(adj_list, members)
    null_nodes = find_null_nodes(adj_list, members)
    adj_list = clean_adj_list(adj_list, junk_nodes, null_nodes)
    removed_len = len(junk_nodes) + len(null_nodes)

    final_len = len(adj_list)

    log('%d items cleaned from adjacancy list' % (init_len - final_len),
        'Notification')
    return adj_list


def create_graph(adj_list):
    """(dict)->module
    dsc: create networkx Graph object form given adjacancy list
    """
    G = Graph()
    G.add_nodes_from(adj_list.keys())
    for name, friends in adj_list.items():
        if friends.__class__ == list:
            edges = zip([name]*len(friends), friends)
            G.add_edges_from(edges)
    return G


def plot_graph(G):
    """()->None
    dsc: plots figure from given networkx graph object and saves it
    """
    plt.figure(figsize=(60, 30))
    pos = nx.graphviz_layout(G, prog="neato")
    draw(G, pos, node_size=100, font_size=2, edge_color='k', alpha=0.8)
    plt.axis('off')
    plt.savefig("friends_graph.svg", format='SVG')


if __name__ == '__main__':

    work = '306947'
    work = '1576656'
    members = books.find_all_members(work)
    adj_list = find_adjacancy_list(work)
    adj_list = make_cleand_adjacancy_list(adj_list)

    # make sure every member of work is in adjacancy list
    for member in members:
        if member not in adj_list:
            log('%s removed from adjacancy list' % member, 'Error')

    G = create_graph(adj_list)
    #print betweenness_centrality(G,normalized=False)
