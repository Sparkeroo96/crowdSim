global mapLocations
class A_Star:
    path = []
    def __init__(self, parent, position):
        self.parent = parent
        self.position = position

        """distance is from current cord to end coord"""

        self.distance = 0
        """heuristic is estimated distance from current node to end node"""
        self.heuristic = 0
        """Cost is total cost of the node (Distance + Heuristic)"""
        self.cost = 0

    """try to identify what eq means"""
    def __eq__(self, other):
        return self.position == other.position


def aStar(maze, start, end):
    # Create start and end node
    start_node = A_Star(None, start)
    start_node.g = start_node.h = start_node.f = 0
    end_node = A_Star(None, end)
    end_node.g = end_node.h = end_node.f = 0

    # Initialize both open and closed list
    open_list = []
    closed_list = []

    # Add the start node
    open_list.append(start_node)

    # Loop until you find the end
    while len(open_list) > 0:
        # Get the current node
        current_node = open_list[0]
        current_index = 0
        for index, item in enumerate(open_list):
            if item.f < current_node.f:
                current_node = item
                current_index = index

        # Pop current off open list, add to closed list
        open_list.pop(current_index)
        closed_list.append(current_node)

        # Found the goal
        if current_node == end_node:
            path = []
            current = current_node
            while current is not None:
                path.append(current.position)
                current = current.parent
            return path[::-1]  # Return reversed path

        # Generate children
        children = []
        i = 2
        for new_position in [(0, -1), (0, 1), (-1, 0), (1, 0), (-1, -1), (-1, 1), (1, -1),
                             (1, 1)]:  # Adjacent squares

            # Get node position
            node_position = (current_node.position[0] + new_position[0], current_node.position[1] + new_position[1])

            # Make sure within range
            if node_position[0] > (len(maze) - 1) or node_position[0] < 0 or node_position[1] > (
                    len(maze[len(maze) - 1]) - 1) or node_position[1] < 0:
                continue

            # Make sure walkable terrain
            if maze[node_position[0]][node_position[1]] != 0:
                continue

            # Create new node
            new_node = A_Star(current_node, node_position)

            # Append
            children.append(new_node)

        # Loop through children
        for child in children:

            # Child is on the closed list
            for closed_child in closed_list:
                if child == closed_child:
                    continue

            # Create the f, g, and h values
            child.g = current_node.g + 1
            child.h = ((child.position[0] - end_node.position[0]) ** 2) + (
                    (child.position[1] - end_node.position[1]) ** 2)
            child.f = child.g + child.h

            # Child is already in the open list
            for open_node in open_list:
                if child == open_node and child.g > open_node.g:
                    continue

            # Add the child to the open list
            open_list.append(child)


"""Returns Locations of nodes we need to travel to"""
def store_node_details(locations):
    global mapLocations
    mapLocations = locations
    # for node in locations:
    #     mapLocations.append((node[0]*50, node[1]*50))
    return mapLocations

"""Returns the mapLocations required"""
def get_details():
    mapLocations = []
    return mapLocations

