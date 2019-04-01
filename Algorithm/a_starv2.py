import numpy
import math
from random import randint
from heapq import *
mapLocations = []
graph = []
finalLocations = []
n = []
heatmap_store = {}

#  The binary heap keeps the open list in order
def astar(array, start, dest):
    """THE DESTINATION WILL BE DEEMED AS A 1"""
    # print("array in astar" + str(array))

    neighbours = [(0, 1), (0, -1), (1, 0), (-1, 0), (1, 1), (-1, -1), (1, -1), (-1, 1)]

    close_set = set()
    # The parent of the node we are currently occupied
    came_from = {}
    # Distance between start node and end node
    start_to_current_score = {start: 0}
    # Total cost of the node
    score_of_node = {start: calculate_heuristic(start, dest)}
    stored_heap = []

    """Push item onto heap, maintaining the heap."""
    heappush(stored_heap, (score_of_node[start], start))
    while stored_heap:
        current_parent = heappop(stored_heap)[1]  # Current parent
        """We have found the destination"""
        if current_parent == dest:
            final_path = []
            while current_parent in came_from:  # While there is still a parent.
                final_path.append(current_parent)
                """" Move from child node to parent node """
                current_parent = came_from[current_parent]
            global mapLocations
            mapLocations = final_path
            mapLocations.reverse()
            # array[(dest[0], dest[1])] = 1
            return final_path  # Return the list
        close_set.add(current_parent)  # Add the current parent to the closed set.
        for x, y in neighbours:
            neighbour = current_parent[0] + x, current_parent[1] + y  # Assign neighbours
            # Create a placeholder g score, adding the distance and heuristic
            placeholder_start_to_current_score = start_to_current_score[current_parent]\
                                                 + calculate_heuristic(current_parent, neighbour)
            if 0 <= neighbour[0] < array.shape[0]:  # If neighbour inside the array
                if 0 <= neighbour[1] < array.shape[1]:
                    """ If the value is 1, this is a node we cannot pass through """
                    if array[neighbour[0]][neighbour[1]] == 1:
                        continue
                else:
                    """ array bound y walls """
                    continue
            else:
                """ array bound x walls """
                continue
            """Ignore this neighbour as they have been added to close set"""
            """Score is greater"""
            if neighbour in close_set and placeholder_start_to_current_score >= start_to_current_score.get(neighbour, 0):
                continue

            #  If the score is lower
            #  If neighbour does not exist in the heap
            if placeholder_start_to_current_score < start_to_current_score.get(neighbour, 0) or \
                    neighbour not in [i[1] for i in stored_heap]:
                came_from[neighbour] = current_parent  # this value will be the new parent
                start_to_current_score[neighbour] = placeholder_start_to_current_score
                score_of_node[neighbour] = placeholder_start_to_current_score + calculate_heuristic(neighbour, dest)
                heappush(stored_heap, (score_of_node[neighbour], neighbour))  # Push the neighbour to the queue
    """Cannot find a path"""
    return False


"""Working out the estimated distance between from current node to end node"""
"""a = start"""
"""b = destination"""
"""a** + b** = heuristic"""
def calculate_heuristic(start, dest):
    return (dest[0] - start[0]) ** 2 + (dest[1] - start[1]) ** 2


"""copies the graph made from map_data to the a_star class"""
def store_all_nodes(g):
    global graph
    graph = g.copy()
    # print("stored" + str(g))

def get_all_nodes():
    global graph
    if len(graph) > 0:
        return graph
    else:
        return False

"""Returns Locations of nodes we need to travel to"""
def store_node_details(locations):
    global mapLocations
    mapLocations = locations
    return mapLocations

"""Converts the maplocations to waypoints it has to follow"""
def return_waypoints(locations):
    waypoints = []
    i = 0
    if locations == False:
        return
    while i < len(locations):
        try:
            if locations[i][0] != locations[i + 1][0] and locations[i][1] != locations[i + 1][1]:
                waypoints.append(locations[i])
            elif locations[i][0] != locations[i - 1][0] and locations[i][1] != locations[i - 1][1]:
                waypoints.append(locations[i])
            elif locations[i + 1][0] == None or locations[i + 1][0] == None:  #These cords are at the edge
                waypoints.append(locations[i])
            elif locations[i + 2][1] == None or locations[i + 2][0] == None:
                pass
            elif locations[i][0] == locations[i + 1][0]:  # Up or Down movement
                if locations[i + 1][0] == locations[i + 2][0]:
                    pass
            elif locations[i][1] == locations[i + 1][1]:  # Left to Right movement
                if locations[i + 1][1] == locations[i + 2][1]:
                    pass
            else:
                waypoints.append(locations[i])
        except IndexError:
                nothing = 1
        i += 1
    if not locations:
        return
    else:
        """Add the destination to the final waypoint"""
        waypoints.append(locations[-1])
    # print("WAYPOINTS ARE: " + str(waypoints))
    global mapLocations
    mapLocations = waypoints
    return waypoints


"""Returns the mapLocations required"""
# def get_details():
#     global mapLocations
#     return mapLocations

"""Needs start and destination coords"""
def run_astar(start, dest):
    a = convert_to_simple(start)
    b = convert_to_simple(dest)
    destx = b[0] + 1
    desty = b[1] + 1
    allNodes = get_all_nodes()
    result = None
    if allNodes is not False and a is not None:
        result = astar(allNodes, a, b)
    if result is False: # Catch if there are no astar coords and attempt to move to the top right node.
        new_dest = destx, desty
        result = astar(allNodes, a, new_dest)
    if result is False: # Catch if there are no astar coords and attempt to move to the bottom left node.
        destxv2 = b[0] - 1
        destyv2 = b[1] - 1
        new_dest_v2 = destxv2, destyv2
        result = astar(allNodes, a, new_dest_v2)
    if result is not None and result is not False:
        if len(result) <= 2:  # At this point, the agent is near enough to the object.
            return False
        waypoint = return_waypoints(store_node_details(result))
        # return store_node_details(result)
        return locations(waypoint)


"""Convert coords that we have as our start and dest to simple 0 - 9 coords."""
def convert_to_simple(cords):
    converted = []
    if cords is None:
        return False
    for c in cords:
        change = math.floor(c / 20)
        if change <= 0:
            change = 0
            converted.append(change)
        else:
            converted.append(change)
    return converted[0], converted[1]

"""Returns the final location waypoints of the algorithm needed. """
def locations(path):
    global finalLocations
    finalLocations = []
    if not path:
        return
    for p in path:
        finalLocations.append((p[0] * 20, p[1] * 20))
    return finalLocations

def set_open_nodes(nodes):
    global n
    for node in nodes:
        n.append([node[0] * 20, node[1] * 20])

def get_open_nodes():
    global n
    return n

def get_random_waypoint():
    """
    Gets a random waypoint
    :return: A random node
    """

    global n
    nodeCount = len(n)
    # randNodeKey = randint(0, nodeCount - 1)

    nodes = get_open_nodes()
    nodes_length = len(nodes)
    return nodes[randint(0, nodes_length - 1)]

    # return n[randNodeKey]

