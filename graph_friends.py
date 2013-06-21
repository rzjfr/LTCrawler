import books
import friends
import json
from HelperMethods import *
from networkx import *
import matplotlib.pyplot as plt
from networkx import graphviz_layout
from datetime import datetime
import matplotlib.pyplot as pyplt
import numpy as np


def friends_list(members):
    """(list)->dict
    dsc: returns friend list for each member of given list
    """
    known = load_local_friends()  # all known usernames
    result = {}
    for member in members:
        result.update({member: known[member]})
    return result


def remove_not_book_member(adj_list, all_members):
    """(dict, list)-> adj_list
    dsc: remove all other member except members in all_members from adj_list
    """
    result = {}
    for name, friends in adj_list.items():
        new_friends = []
        for friend in friends:
            if friend in all_members:
                new_friends.append(friend)
        result.update({name: new_friends})
    return result


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
    file_path = './data/%s_members.json' % work
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


def make_cleand_adjacancy_list(adj_list, members):
    """(dict, list)->dict
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


def plot_graph(G, a, b):
    """()->None
    dsc: plots figure from given networkx graph object and saves it
    """
    colors = []
    for v in G:
        if v in a and v in b:
            colors.append('b')
        elif v in a:
            colors.append('r')
        elif v in b:
            colors.append('g')
        else:
            colors.append('y')
    time_stamp = str(datetime.now())
    plt.figure(figsize=(120, 120))
    #pos = nx.graphviz_layout(G, prog="neato")
    #pos = graphviz_layout(G, prog="twopi", root='AsYouKnow_Bob')
    draw(G, pos, node_size=100, font_size=4, edge_color='k', alpha=0.8,
         node_color=colors, linewidths=0, width=0.2, edge_cmap=plt.cm.Blues)
    plt.axis('off')
    #plt.savefig("./figures/friends_graph_%s.svg" % time_stamp, format='SVG')
    plt.savefig("./figures/friends_graph_%s.png" % time_stamp, format='PNG')
    #plt.savefig("./figures/friends_graph_%s.pdf" % time_stamp, format='PDF')


def plot_hist(G):
    """(object)->None
    dsc: plots degree for each user
    """
    nodes_degree = [(i, len(G.neighbors(i))) for i in G.nodes()]
    nodes_degree = sorted(nodes_degree, key=lambda x: x[1], reverse=True)
    a = [i for i, j in nodes_degree]
    b = [j for i, j in nodes_degree]
    pos = np.arange(len(a))
    #width = 1.0
    time_stamp = str(datetime.now())
    pyplt.figure(figsize=(300, 10))
    ax = pyplt.axes()
    ax.set_xticks(pos)
    ax.set_xticklabels(a, rotation=30, size='small')
    plt.bar(pos, b, color='r')
    plt.savefig("./figures/degree_freq_%s.png" % time_stamp, format='PNG')


def average_shortest_path_between(G, members_a, members_b):
    """(object, list, list)->float
    dsc: average of shortest path between to list of members
    """
    result = []
    for member_a in remove_duplicate(members_a):
        for member_b in remove_duplicate(members_b):
            if has_path(G, member_a, member_b):
                result.append(len(shortest_path(G, member_a, member_b)))
            elif G.neighbors(member_a) == []:
                result.append(0)
    # find average for list
    return sum(result)/float(len(result))


def same_users_between(members_a, members_b):
    """(list, list)->list
    dsc: returns a list of same users in two givn lists
    """
    result = []
    for member in remove_duplicate(members_a):
        if member in members_b:
            result.append(member)
    return remove_duplicate(result)


def save_edges(G, d=False, name=''):
    """
    dsc: save all edges in a text file
    """
    time_stamp = str(datetime.now())
    if name != '':
        file_name = './data/graph/%s.edges' % name
    else:
        name = 'graph' + time_stamp
        file_name = './data/graph/%s.edges' % name

    f = open(file_name, 'wb')
    write_edgelist(G, f, data=d)
    write_gexf(G, "./data/graph/graph%s%s.gexf" % (name, time_stamp))


def analysis_1(work_a, work_b):
    members_a = books.find_all_members(work_a)
    adj_list = find_adjacancy_list(work_a)
    adj_list = make_cleand_adjacancy_list(adj_list, members_a)

    # make sure every member of work is in adjacancy list
    for member in members_a:
        if member not in adj_list:
            log('%s removed from adjacancy list of %s' % (member, work_a),
                'Error')

    members_b = books.find_all_members(work_b)
    adj_list_b = find_adjacancy_list(work_b)
    adj_list_b = make_cleand_adjacancy_list(adj_list_b, members_b)

    # make sure every member of work is in adjacancy list
    for member in members_b:
        if member not in adj_list_b:
            log('%s removed from adjacancy list of %s' % (member, work_b),
                'Error')

    # create the big adjacanvy list for mambers of both books
    adj_list.update(adj_list_b)

    G = create_graph(adj_list)
    save_edges(G, True, 'all_friends')
    #print betweenness_centrality(G,normalized=False)
    print '%s has %d members' % (work_a, len(remove_duplicate(members_a)))
    print '%s has %d members' % (work_b, len(remove_duplicate(members_b)))
    same = same_users_between(members_a, members_b)
    print 'and %s of them are in both works' % len(same)
    #avg = average_shortest_path_between(G, members_a, members_b)
    #print 'average shortest path between %s and %s %f' % (work_a, work_b, avg)
    #avg = average_shortest_path_between(G, members_a, members_a)
    #print 'average shortest path between members of %s is %f' % (work_a, avg)
    #avg = average_shortest_path_between(G, members_b, members_b)
    #print 'average shortest path between members of %s is %f' % (work_b, avg)
    return G


def analysis_2(work_a, work_b):
    members_a = books.find_all_members(work_a)
    print len(remove_duplicate(members_a))
    members_b = books.find_all_members(work_b)

    adj_list = friends_list(members_a)
    adj_list = make_cleand_adjacancy_list(adj_list, members_a)

    #G1 = create_graph(remove_not_book_member(adj_list, members_a))
    #plot_graph(G1, members_a, members_b)
    adj_list_b = friends_list(members_b)
    adj_list_b = make_cleand_adjacancy_list(adj_list_b, members_b)

    #G2 = create_graph(remove_not_book_member(adj_list_b, members_b))
    #plot_graph(G2, members_a, members_b)
    adj_list.update(adj_list_b)
    all_members = remove_duplicate(members_a + members_b)
    adj_list = remove_not_book_member(adj_list, all_members)

    print len(adj_list)
    G = create_graph(adj_list)
    #plot_graph(G, members_a, members_b)
    #save_edges(G)
    GC = connected_component_subgraphs(G)[0]  # Giant Component
    center = sort_dict(closeness_centrality(GC))[0]
    #center = sort_dict(eigenvector_centrality(GC))[0]
    #center = sort_dict(betweenness_centrality(GC))[0]
    #pos = graphviz_layout(G, prog="twopi", root=center)  # draw and save
    #plot_graph(GC, members_a, members_b)
    return G


if __name__ == '__main__':
    work_a = '306947'  # The Holy Bible: King James Version (KJV)
    work_b = '1576656'  # The Blind Watchmaker
    members_a = books.find_all_members(work_a)
    members_b = books.find_all_members(work_b)
    #G = analysis_1(work_a, work_b)
    #G = analysis_2(work_a, work_b)
    #C = connected_component_subgraphs(G)[0]  # Giant Component
    #plot_hist(C)
