from room import Room
from player import Player
from world import World
from util import Stack, Queue


import random
from ast import literal_eval

SOUTH_KEY = 's'
NORTH_KEY = 'n'
WEST_KEY = 'w'
EAST_KEY = 'e'

def breadthFirstSearch(graph, starting_vertex):
    """
    Print each vertex in breadth-first order
    beginning from starting_vertex.
    """
    #pass  # TODO
    # take starting vertex
    # print all neighbours
    # then go to each neighbour and print all neighbours


    queue = Queue()
    seenBefore = set()
    queue.enqueue([starting_vertex])
    while queue.size() > 0:
        current = queue.dequeue()
        # print("current is ", current)
        last_vertex = current[-1]

        if last_vertex not in seenBefore:
            neighbors = get_neighbors(graph, last_vertex)
            for each in neighbors:
                new_path = list(current)
                new_path.append(each)
                queue.enqueue(new_path)
                if each == '?':
                    return new_path
            seenBefore.add(last_vertex)



def get_neighbors(graph, room):
    neighbors = list(graph[room].values())
    return neighbors

def nearest_unexplored_room(graph, room):
    unexplored_room_path = breadthFirstSearch(graph, room)
    if unexplored_room_path is None:
        return None
    # print("path of ids is ", unexplored_room_path)
    #need to convert into useable direction format

    path = []

    for i in range(0, len(unexplored_room_path) - 1):
        #print("this is", graph[unexplored_room_path[i]])
        graph_list = list(graph[unexplored_room_path[i]].items())
        # print("graph list is ", graph_list)
        for each in graph_list:
            if each[1] == unexplored_room_path[i+1] and each[1] != '?':
                # print("each: ", each[1], "item: ", unexplored_room_path[i+1])
                path.append(each[0])
    return path


def unexplored_exit(value):
    if value == '?':
        return True
    else:
        return False

def create_path():
    player = Player(world.starting_room)
    seenBefore = set()
    stack = Stack()
    traversal_path = []
    graph = {}
    opposites = {'n': 's', 's':'n', 'w':'e', 'e': 'w'}


    graph[player.current_room.id] = {}

    current_exits = player.current_room.get_exits()
    for each in current_exits:
        graph[player.current_room.id][each] = '?'
    
    unexplored_directions = [entry[0] for entry in list(
        graph[player.current_room.id].items()) if entry[1] == '?']
    

    if SOUTH_KEY in unexplored_directions:
        move_direction = SOUTH_KEY
    else:
        move_direction = unexplored_directions[chooseDirection(unexplored_directions)]


    stack.push(move_direction)

    while stack.size() > 0:
        current_move = stack.pop()
        prev_room = player.current_room.id
        traversal_path.append(current_move)
        # print("traversal path is currently:", traversal_path)
        player.travel(current_move)

        current_exits = player.current_room.get_exits()
        #print(current_exits)

        if player.current_room.id not in seenBefore:
            graph[player.current_room.id] = {}
            # print("current room exits r", current_exits)
            for each in current_exits:
                graph[player.current_room.id][each] = '?'
            seenBefore.add(player.current_room.id)
            
        opposite_direction = opposites[current_move]
        graph[player.current_room.id][opposite_direction] = prev_room
        graph[prev_room][current_move] = player.current_room.id
        # print("prev room id", graph[player.current_room.id][opposite_direction])
        # print("current room id", player.current_room.id)
            
        unexplored_exits = []
        current_directions = graph[player.current_room.id].items()
        for each in current_directions:
            if unexplored_exit(each[1]):
                unexplored_exits.append(each[0])

        # print("unexplored directions are ", unexplored_exits)
        if len(unexplored_exits) > 0:
            if SOUTH_KEY in unexplored_exits:
                move_direction = SOUTH_KEY
            else:
                move_direction = unexplored_exits[chooseDirection(unexplored_exits)]
            stack.push(move_direction)
            # print("move direction is ", move_direction)
        else:
            next_room_path = nearest_unexplored_room(graph, player.current_room.id)
            # print("current room exits r", current_exits)
            if next_room_path is None: 
                return traversal_path

            # print("next pathway is", next_room_path)
            for i in range(0, len(next_room_path)-1):
                player.travel(next_room_path[i])
                # print(player.current_room.get_exits())
                traversal_path.append(next_room_path[i])
                seenBefore.add(player.current_room.id)
            stack.push(next_room_path[-1])

    return traversal_path


        



def chooseDirection(directionsList):
    return random.randint(0, len(directionsList) - 1)




# Load world
world = World()


# You may uncomment the smaller graphs for development and testing purposes.
# map_file = "maps/test_line.txt"
# map_file = "maps/test_cross.txt"
# map_file = "maps/test_loop.txt"
# map_file = "maps/test_loop_fork.txt"
map_file = "maps/main_maze.txt"

# Loads the map into a dictionary
room_graph=literal_eval(open(map_file, "r").read())
world.load_graph(room_graph)

# Print an ASCII map
world.print_rooms()

player = Player(world.starting_room)

# Fill this out with directions to walk
# traversal_path = ['n', 'n']
#traversal_path = []




traversal_path = create_path()
# TRAVERSAL TEST - DO NOT MODIFY
visited_rooms = set()
player.current_room = world.starting_room
visited_rooms.add(player.current_room)

for move in traversal_path:
    player.travel(move)
    visited_rooms.add(player.current_room)

if len(visited_rooms) == len(room_graph):
    print(f"TESTS PASSED: {len(traversal_path)} moves, {len(visited_rooms)} rooms visited")
else:
    print("TESTS FAILED: INCOMPLETE TRAVERSAL")
    print(f"{len(room_graph) - len(visited_rooms)} unvisited rooms")



#######
# UNCOMMENT TO WALK AROUND
#######
player.current_room.print_room_description(player)
while True:
    cmds = input("-> ").lower().split(" ")
    if cmds[0] in ["n", "s", "e", "w"]:
        player.travel(cmds[0], True)
    elif cmds[0] == "q":
        break
    else:
        print("I did not understand that command.")
