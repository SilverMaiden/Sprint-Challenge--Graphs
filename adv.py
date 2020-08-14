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

    paths = []
    seenBefore = set()

    queue.enqueue([starting_vertex])

    while queue.size() > 0:
        current = queue.dequeue()
        print("current is ", current)
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

    #need to convert into useable direction format

    path = []

    myList = []

    for i, each in enum(unexplored_room_path):
        possible_directions = graph[each].items()

        for direction in possible_directions:
            if direction[1] == unexplored_room_path[i + 1]:
                path.append(direction[0])
    return path




def create_path():
    player = Player(world.starting_room)
    seenBefore = set()
    stack = Stack()
    traversal_path = []
    graph = {}

    graph[player.current_room.id] =  {}
    #seenBefore.add(player.current_room.id)

    stack.push(player.current_room)

    while len(seenBefore) < len(graph):
        current_room = stack.pop()
        if current_room.id not in seenBefore:
            seenBefore.add(current_room.id)
            current_room_exits = current_room.id.get_exits()

            for each in current_room_exits:
                graph[current_room.id][each] = '?'
        else:
            next_room = nearest_unexplored_room(graph, current_room)


    #Go south if possible, depth first

        if SOUTH_KEY in current_room_exits:
            next_direction = SOUTH_KEY
            next_room = current_room.s_to()
        else:
            next_direction = current_room_exits[chooseDirection(current_room_exits)]
            if next_direction == 'n':
                next_room = current_room.n_to()
            elif next_direction == 'e':
                next_room = current_room.e_to()
            elif next_direction == 'w':
                next_room = current_room.w_to()
        traversal_path.append(next_direction)
        stack.push(next_room)

    


        # else:
        #     through_exit_room_id = player.current_room.get_room_in_direction(each)
        #     graph[player.current_room.id][each] = through_exit_room_id


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
traversal_path = []





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
