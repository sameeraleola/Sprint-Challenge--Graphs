from room import Room
from player import Player
from world import World

import random
from ast import literal_eval

# Load world
world = World()

# # Create the queue
# class Queue:
#     def __init__(self):
#         self.queue = []
#     def enqueue(self, value):
#         self.queue.append(value)
#     def dequeue(self):
#         if self.size() > 0:
#             return self.queue.pop(0)
#         else:
#             return None
#     def size(self):
#         return len(self.queue)

# Properties
class Stack():
    def __init__(self):
        self.stack = []
    def push(self, value):
        self.stack.append(value)
    def pop(self):
        if self.size() > 0:
            return self.stack.pop()
        else:
            return None
    def size(self):
        return len(self.stack)

s = Stack()
room_num = 0
visited = {0: {}}
dirs = {'n': 's', 's': 'n', 'e': 'w', 'w': 'e'}

# You may uncomment the smaller graphs for development and testing purposes.
# map_file = "maps/test_line.txt"
# map_file = "maps/test_cross.txt"
# map_file = "maps/test_loop.txt"
# map_file = "maps/test_loop_fork.txt"
map_file = "maps/main_maze.txt"

# Loads the map into a dictionary
room_graph = literal_eval(open(map_file, "r").read())
world.load_graph(room_graph)

# Print an ASCII map
world.print_rooms()

player = Player(world.starting_room)

# Fill this out with directions to walk
# traversal_path = ['n', 'n']
traversal_path = []

def get_next(traversal_path, visited, this_room, s, dirs):
    while True:
        to_next = s.pop()
        traversal_path.append(to_next)
        next_room = this_room.get_room_in_direction(to_next)
        if 'v' in visited[next_room.id].values():
            return next_room.id
        this_room = next_room
print(f'traversal_path = {traversal_path}') 
def find_next(visited, urhere):
    this_room = urhere.id
    room_exits = visited[this_room]
    for room_dir in room_exits:
        if room_exits[room_dir] == 'v' and urhere.get_room_in_direction(room_dir).id not in visited:
            return room_dir
    return None

this_room = world.rooms[room_num]

for room_dir in this_room.get_exits():
    visited[this_room.id][room_dir] = 'v'

while len(visited) < len(world.rooms):
    this_room = world.rooms[room_num]
    if this_room not in visited:
        visited[this_room.id] = {}
        for room_dir in this_room.get_exits():
            visited[this_room.id][room_dir] = 'v'
    to_next = find_next(visited, this_room)
    if not to_next:
        room_num = get_next(traversal_path, visited, this_room, s, dirs)
    else:
        traversal_path.append(to_next)
        next_room = this_room.get_room_in_direction(to_next)
        visited[room_num][to_next] = next_room.id
        if next_room.id not in visited:
            visited[next_room.id] = {}
            for room_dir in next_room.get_exits():
                visited[next_room.id][room_dir] = 'v'
        visited[next_room.id][dirs[to_next]] = this_room.id
        s.push(dirs[to_next])
        room_num = next_room.id

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
