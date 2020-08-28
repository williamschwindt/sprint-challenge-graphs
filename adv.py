from room import Room
from player import Player
from world import World

import random
from ast import literal_eval

# Load world
world = World()


# You may uncomment the smaller graphs for development and testing purposes.
# map_file = "maps/test_line.txt"
# map_file = "maps/test_cross.txt"
map_file = "maps/test_loop.txt"
# map_file = "maps/test_loop_fork.txt"
# map_file = "maps/main_maze.txt"

# Loads the map into a dictionary
room_graph=literal_eval(open(map_file, "r").read())
world.load_graph(room_graph)

# Print an ASCII map
world.print_rooms()

player = Player(world.starting_room)

# Fill this out with directions to walk
# traversal_path = ['n', 'n']
traversal_path = []
visited = set()
previously_visited_direction = None

def dft(first_move = False):
    global previously_visited_direction
    #if first move is true
    if first_move:
        #pick a random direction and add opposite direction to prev_visited_direciton
        paths = player.current_room.get_exits()
        path = random.choice(paths)
        if path == 'n':
            previously_visited_direction = 's'
        elif path == 'e':
            previously_visited_direction = 'w'
        elif path == 's':
            previously_visited_direction = 'n'
        elif path == 'w':
            previously_visited_direction = 'e'
        #return direction
        return path

    #if not first move 
    else:
        #find all paths
        paths = player.current_room.get_exits()
        #remove the prev_direction from paths
        paths.remove(previously_visited_direction)
        #remove the directions that would lead to a previously visited room
        for path in paths:
            if player.current_room.get_room_in_direction(path) in visited:
                paths.remove(path)
        #if paths > 0
        if len(paths) > 0:
            #pick random path
            path = random.choice(paths)
            #set prev_direction to opposite of path
            if path == 'n':
                previously_visited_direction = 's'
            elif path == 'e':
                previously_visited_direction = 'w'
            elif path == 's':
                previously_visited_direction = 'n'
            elif path == 'w':
                previously_visited_direction = 'e'
            #return direction
            return path
        #if no paths
        if len(paths) == 0:
            #return false
            return False

def adv():
    print(player.current_room)
    #add cur room to visited
    visited.add(player.current_room)
    #call dft with first move set to true
    direction = dft(True)
    traversal_path.append(direction)
    player.travel(direction)

    playing = True
    #while loop
    while playing:
        print(player.current_room)
        visited.add(player.current_room)
        #call dft
        direction = dft()
        #check if there is a unexplored path
        #if not stop dft
        if direction == False:
            playing = False
        #if there is then travel
        else:
            traversal_path.append(direction)
            player.travel(direction)

adv()





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
# player.current_room.print_room_description(player)
# while True:
#     cmds = input("-> ").lower().split(" ")
#     if cmds[0] in ["n", "s", "e", "w"]:
#         player.travel(cmds[0], True)
#     elif cmds[0] == "q":
#         break
#     else:
#         print("I did not understand that command.")
