import numpy
import math
from random import randint
from heapq import *
mapLocations = []
test = (1, 1), (-1, -1), (1, -1), (-1, 1)
graph = []
finalLocations = []
n = []
heatmap_store = {}

#  The binary heap keeps the open list in order
def astar(array, start, dest):
    """THE DESTINATION WILL BE DEEMED AS A 1"""
    print("array in astar" + str(array))

    neighbours = [(0, 1), (0, -1), (1, 0), (-1, 0), (1, 1), (-1, -1), (1, -1), (-1, 1)]

    close_set = set()
    # The parent of the node we are currently occupied
    came_from = {}
    # Distance between start node and end node
    gscore = {start: 0}
    # Total cost of the node
    fscore = {start: heuristic(start, dest)}
    oheap = []

    heappush(oheap, (fscore[start], start))

    while oheap:
        current = heappop(oheap)[1]  # Current parent

        if current == dest:  # The current Parent is the destination
            data = []
            while current in came_from:  # While there is still a parent.
                data.append(current)
                current = came_from[current]  # Move from child node to parent node
            global mapLocations
            mapLocations = data
            mapLocations.reverse()
            # array[(dest[0], dest[1])] = 1
            return data  # Return the list

        close_set.add(current)  # Add the current parent to the closed set.
        for i, j in neighbours:
            neighbour = current[0] + i, current[1] + j  # Assign neighbours

            # Create a placeholder g score, adding the distance and heuristic
            tentative_g_score = gscore[current] + heuristic(current, neighbour)
            if 0 <= neighbour[0] < array.shape[0]:  # If neighbour inside the array
                if 0 <= neighbour[1] < array.shape[1]:
                    if array[neighbour[0]][neighbour[1]] == 1:  # If the value is 1, this is a wall
                        continue
                else:
                    # array bound y walls
                    continue
            else:
                # array bound x walls
                continue

            if neighbour in close_set and tentative_g_score >= gscore.get(neighbour, 0):
                continue

            #  If the score is lower
            #  If neighbour does not exist in the heap
            if tentative_g_score < gscore.get(neighbour, 0) or neighbour not in [i[1] for i in oheap]:
                came_from[neighbour] = current  # this value will be the new parent
                gscore[neighbour] = tentative_g_score
                fscore[neighbour] = tentative_g_score + heuristic(neighbour, dest)
                heappush(oheap, (fscore[neighbour], neighbour))  # Push the neighbour to the queue

    return False


"""Working out the estimated distance between from current node to end node"""
"""a = start"""
"""b = destination"""
"""a** + b** = heuristic"""
def heuristic(a, b):
    return (b[0] - a[0]) ** 2 + (b[1] - a[1]) ** 2


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
                print("")
        i += 1
    if not locations:
        return
    else:
        """Add the destination to the final waypoint"""
        waypoints.append(locations[-1])
    print("WAYPOINTS ARE: " + str(waypoints))
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
    """Convert coords to the node boys"""
    allNodes = get_all_nodes()
    result = None
    if allNodes is not False:
        result = astar(allNodes, a, b)


    if result is None:
        return print("none")
    else:
        waypoint = return_waypoints(store_node_details(result))
        # return store_node_details(result)
        return locations(waypoint)


"""Convert coords that we have as our start and dest to simple 0 - 9 coords."""
def convert_to_simple(cords):
    converted = []
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
    randNodeKey = randint(0, nodeCount - 1)

    nodes = get_open_nodes()
    nodes_length = len(get_open_nodes())
    return nodes[randint(0, nodes_length - 1)]

    # return n[randNodeKey]
