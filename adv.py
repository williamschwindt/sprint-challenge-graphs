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

def random_direction(first_move = False):
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

def bft_search():
    global visited
    starting_room = player.current_room
    #create an empty queue and enqueue the starting room as a list
    path_queue = []
    path_queue.append([starting_room])
    #while the queue isnt empty
    while len(path_queue) > 0:
        #get the current path
        cur_path = path_queue[0]
        #remove from queue
        path_queue.pop(0)
        #set current room to last room in cur path
        cur_room = cur_path[-1]
        #check if that room has been visited
        if cur_room not in visited:
            #if not return the path to the room
            cur_path.pop(0)
            backtrack_path = []


            for i in range(0, len(cur_path)):
                if starting_room.get_room_in_direction('n') == cur_path[i]:
                    starting_room = cur_path[i]
                    backtrack_path.append('n')
                elif starting_room.get_room_in_direction('e') == cur_path[i]:
                    starting_room = cur_path[i]
                    backtrack_path.append('e')
                elif starting_room.get_room_in_direction('s') == cur_path[i]:
                    starting_room = cur_path[i]
                    backtrack_path.append('s')
                elif starting_room.get_room_in_direction('w') == cur_path[i]:
                    starting_room = cur_path[i]
                    backtrack_path.append('w')






            return backtrack_path
        #if it has been visited add path to neighbors to queue
        if cur_room in visited:
            for direction in cur_room.get_exits():
                new_path = list(cur_path)
                new_path.append(cur_room.get_room_in_direction(direction))
                path_queue.append(new_path)

def adv():
    print(player.current_room)
    #add cur room to visited
    visited.add(player.current_room)
    #call random_direction with first move set to true
    direction = random_direction(True)
    traversal_path.append(direction)
    player.travel(direction)

    playing = True
    dft = True
    bft = True
    #while loop
    while playing:
        #dft traversal
        while dft:
            print(player.current_room)
            visited.add(player.current_room)
            #call random_direction
            direction = random_direction()
            #check if there is a unexplored path
            #if not stop random_direction
            if direction == False:
                dft = False
            #if there is then travel
            else:
                traversal_path.append(direction)
                player.travel(direction)

        #bft traversal
        while bft:
            print(player.current_room)
            visited.add(player.current_room)
            #call bft search to find path to nearest unknown location
            backtrack_path = bft_search()
            print('bft', backtrack_path)
            bft = False
            playing = False
            #travel back to that locaiton
            #start dft again


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
