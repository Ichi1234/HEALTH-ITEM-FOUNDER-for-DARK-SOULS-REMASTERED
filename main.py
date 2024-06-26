# 31 vertices , 66 edges in real data


# this example similar to my real data
adj = {0: [(1, 10), (2, 2), (3, 7), (4, 4)], 1: [(0, 10), (4, 4)], 2: [(0, 2), (3, 2), (4, 5)],
       3: [(0, 7), (2, 2), (4, 1)], 4: [(0, 4), (1, 4), (2, 5), (3, 1)]}

items_container = [2, 0, 2, 3, 1]
output_items = [2, 0, 2, 3, 1]
current_amount_of_items = []
dist = []
bag = []
shortest_path = {0: [], 1: [], 2: [],
                 3: [], 4: []}


# Printing the adjacency list
def show_adj():
    """this function use to show relationship between each vertex"""
    for node, neighbors in adj.items():
        print(f"adj[{node}]:", end=" ")
        for neighbor, weight in neighbors:
            print(f"({neighbor}, {weight})", end=" ")
        print()


def decrease_key(vertex_id, new_distance):
    """Use for update new distance for bag"""
    for i, (vertex_in_bag, dist_v) in enumerate(bag):
        if vertex_in_bag == vertex_id:
            bag[i] = (vertex_id, new_distance)
            break
    bag.sort(key=lambda x: x[1])  # sort bag base on distance


def item_finder_dijkstra(first_vertex, find_num_items, best_path=None):
    """This code is base on dijikstra algorithm. However, this algorithm aims to find which paths
    is the shortest path and best path to find num_items that are in each vertex"""
    shortest_path.update({0: [], 1: [], 2: [],
                          3: [], 4: []})
    dist.clear()
    bag.clear()
    current_amount_of_items.clear()

    for _ in range(len(adj)):
        dist.append(9999999)  # set initial value
        current_amount_of_items.append([])

    dist[first_vertex] = 0  # set first vertex

    for j in range(len(adj)):
        bag.append((j, dist[j]))

    bag.sort(key=lambda x: x[1])  # put first_vertex that user choose to front of the list

    if items_container[first_vertex] >= find_num_items:
        try:
            return best_path + shortest_path[first_vertex][1:]

        except TypeError:
            return [first_vertex]

    while bag:
        u = bag.pop(0)[0]
        for num_pair in adj[u]:
            v = num_pair[0]
            weight = num_pair[1]

            # choose path that higher item or path that shorter
            if items_container[u] / (dist[u] + weight) > items_container[v] / (dist[v] + 1e-9) or \
                    dist[u] + weight < dist[v]:
                dist[v] = dist[u] + weight
                decrease_key(v, dist[v])
                shortest_path[v].append(u)  # add connect vertex and amount of items
                current_amount_of_items[v].append(items_container[u])

    # add end vertex to shortest_path variable
    for index, value in shortest_path.items():
        if value:
            value.append(index)
            current_amount_of_items[index].append(items_container[index])

    # find which path is shortest
    result_path = [(i, items) for i, items in enumerate(current_amount_of_items) if
                   items and sum(items) >= find_num_items]

    # if the path >= num_items return it else back tracking to find more item
    if result_path:
        result = min(result_path, key=lambda x: len(x[1]))  # Return the path with the minimum length
        try:
            return best_path + shortest_path[result[0]][1:]

        except TypeError:
            return shortest_path[result[0]]

    else:
        # back tracking
        recursive_path = max(enumerate(current_amount_of_items),
                             key=lambda x: sum(x[1]))  # The path with the maximum item sum
        target_path = shortest_path[recursive_path[0]]

        for i in target_path:
            items_container[i] = 0

        return item_finder_dijkstra(recursive_path[0], find_num_items - sum(recursive_path[1]),
                                    shortest_path[recursive_path[0]])


start = int(input("What is the start vertex (int)? "))
user_desired = int(input("How many do you want to find? "))

if user_desired > sum(items_container) or start > len(adj):
    print("Invalid item or vertex!")

else:
    vertex = item_finder_dijkstra(start, user_desired)

    print()
    print(f"Shortest path to find {user_desired} items is ")

    output = " -> ".join(list(map(str, vertex)))
    if "->" in output:
        print(output)
    else:
        print(f"{start} -> {start} (Items is in your area)")

    print(f"Total items: {sum([output_items[i] for i in vertex])}")
