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


def plot_graph(G):
    """()->None
    dsc: plots figure from given networkx graph object and saves it
    """
    plt.figure(figsize=(60, 30))
    pos = nx.graphviz_layout(G, prog="neato")
    draw(G, pos, node_size=100, font_size=2, edge_color='k', alpha=0.8)
    plt.axis('off')
    plt.savefig("friends_graph.svg", format='SVG')


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


if __name__ == '__main__':
    work_a = '306947'  # The Holy Bible: King James Version (KJV)
    members_a = books.find_all_members(work_a)
    adj_list = find_adjacancy_list(work_a)
    adj_list = make_cleand_adjacancy_list(adj_list, members_a)

    # make sure every member of work is in adjacancy list
    for member in members_a:
        if member not in adj_list:
            log('%s removed from adjacancy list of %s' % (member, work_a),
                'Error')

    work_b = '1576656'  # The Blind Watchmaker
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
    # print some usful statistics about Graph G
    #print betweenness_centrality(G,normalized=False)
    print '%s has %d members' % (work_a, len(remove_duplicate(members_a)))
    print '%s has %d members' % (work_b, len(remove_duplicate(members_b)))
    same = same_users_between(members_a, members_b)
    print 'and %s of them are in both works' % len(same)
    avg = average_shortest_path_between(G, members_a, members_b)
    print 'average shortest path between %s and %s  %f' % (work_a, work_b, avg)
    avg = average_shortest_path_between(G, members_a, members_a)
    print 'average shortest path between members of %s is %f' % (work_a, avg)
    avg = average_shortest_path_between(G, members_b, members_b)
    print 'average shortest path between members of %s is %f' % (work_b, avg)
