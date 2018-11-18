
import copy
import codecs
from PIL import Image

# Maze.txt -----> Maze file 
maze_file_loc = 'Maze.txt'
# Maze_solution.txt --------> solution file (generated by the program)
soln_file_loc = 'Maze_solution.txt'
# View the solution file in notepad++ for best results
# character 'S' in the maze file is treated as start location (Should be present in Maze.txt file)
# character 'G' in the maze file is treated as goal location (Should be present in Maze.txt file)
# All 'X' characters in the maze are considered as bloced locations
blocked_tile = 'X'
# All blank spaces are considered as path in the maze
free_tile = ' '
# Program written By : Guru Sarath - 14 Sep 2018 - 7:31 PM
Author = 'T. Guru Sarath\n'
Extra_Text = ''

# Sample Maze.txt would look something like this (Note the 'S' and 'G' positions)
#
#                                                                        'G' position
#                                                                              v
#XXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXX            XXXXXXXXXXXXXXXXXXXXXXXGXXXXXX
#XXXXXXX XXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXX XXXXXXXXXX XXXXXXXXXXXXXXXX        XXXXXX
#XXXXXXX XXXXX XXXXXXXXXXXXXXXXXXXXXXXXXXXXX XXXXXXXXXX XXXXX   XXXXXXXX XXXXXXXXXXXXX
#XXXXXXX             XXXXXXXX                XXXXXXXXXX XXXXX XXXXXXXXXX XXXXXXXXXXXXX
#XXXXXXX XXXXX XXXXX XXXXXXXX XXXXXXXXXXXXXX XXXXXXXXXX XXXXX XXXXXXXXXX          XXXX
#XXXXXXX  XXXXXXXXXX          XXXXXXXXXXXXXX XXXXXXXXXX XXXXX XXXXXXXXXXXXXXXXXXX XXXX
#XXXXXXX XXXXXXXXXXX XXXXXXXXXXXXXXXXXXXXXXX XXX        XXXXX XXXXXXXXXXXXXXXXXXX    X
#XXXXXXX XXXXXXXXXXX XXXXXXXXXXXXXXXXXXXXXXX XXX XXXXXXXXXXXX XXXXXXXXXXXXXXXXXXX XXXX
#XXXXXX  XXXXXXXXXXX XXXXXXXXXXXX                  XXXXX      XXXXXXXXXXX         XXXX
#XXXXXX XXXXXXXXXXXX XXXXXXXXXXXX XXXXXXXXXXXXXXXX XXXXX XXXXXXXX XXXXXXX XXXXXXXXXXXX
#XXXXXX XXXXXXXXXXXX XXXXXXXXXXXX XXXXXXXXXXXXXXXX XXXXX XXXXXXXX XXXXXXX XXXXXXXXXXXX
#XXXXXX XXXXXXXXXXXX XXXXXXXXXXXX XXXXXXXXXXXXXXXX XXXXX XXXXXXXX XXXXXXX XXXXXXXXXXXX
#XXXXXX XXXXXXXX                  XXXXXXXXXXXXXXXX                XXXXXXX XXXXXXXXXXXX
#XXXXXX XXXXXXXX XXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXX XXXXXXX XXXXXXXXXXXXXX XXXXXXXXXXXX
#                XXX XXXXXXXX                    X XXXXXXX XXXXXXXXXXXXXX XXXXXXXXXXXX
#XX XXX XXXXXXXX X     XXXXXX XXXXXXXXXXXXXXXXXX X XXXXXXX XXXXXX     XXX XXXXXXXXXXXX
#XX XXX XXXXXXXX X XXXXXXXXXX XXXXXXXXXXXXXXXXXX X XXXXXXX XXXXXX XXX XXX XXXX     XXX
#XX XXX XXXXXXXX               XXXXXXXXXXX       X XXXXXXX XXXXXX XXX XXX XXXXXXXX XXX
#XX XXX XXXXXXXXXX XXXXXXXXXXXXXX XXXXXXXX XXXXXXX XXXXXXXXXXXXXX XXX     XXXXXXXX XXX
#XX XXX XXXXXXXXXXXXXXXXXXXX XXXX XXXXXXXX XXXXXXX                XXXXXXXXXXXXXXXX XXX
#XX XXX XXXXXXXXXXXXXXXXXX         XXXXXXX XXXXXXX XXXXXXXXXXXXXXXXXXXXXXXXXXXXXXX XXX
#XX XXX XXXXXXXXXXXXXXXXXXXX XXXXX XXXXXXX XXXXXXX XXXXXXXXXXXXXXXXXXXXXXXXXXX     XXX
#XX       XXXXXXXXXXXXXXXXXX XXXXX XXXXXXX XXXXXXX XXXXXXXXXXXXXXXXXXXXXXXXXXX XXXXXXX
#XX XXX XXXXXX        XXXXXX XXXXX XXXXXXX XXXXXXX                XXXX     XXX XXXXXXX
#XXXXXX XXXXX  XXXXXX XXXXXXXXXXXX XXX XXX XXXXXXX XXXX XXXXXXXXX XXXX XXX XXX XXXXXXX
#XXXXXX XXXXX XXXXXXX        XXXXX XXX XXX XXXXXXX XXXX XXXXXXXXX      XXX     XXXXXXX
#XXXXXX       XXXXXXXXXXXXXX XXXXX   X   X XXXXXXX XXXX XXXXXXXXX XXXXXXXXXXXXXXXXXXXX
#XXXXXX XXXXXXXXXXXXXXXXXXXX       X   X   XXXXXXX XXXX XXXXXXXXX XXXXXXXXXXXXXXXXXXXX
#XXXXXXSXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXX XXXXXXXXXXXXXXXXXXXXXXXX XXXXXXXXXXXXXXXXXXXX
#      ^
#  'S' postion


# To enable and disable tracing
ACT = False

# Function to trace the program flow
def traceX(active, strg):
	if active == True:
		print(strg)

# Calculate the heuristic value of the function (Lesser the better)
def Heuristic_calc(state1, state2):
	# Manhattan distance
	M_distance = abs(state1[0] - state2[0]) + abs(state1[1] - state2[1])
	# Euclidian distance
	L_distance = ((state1[1] - state2[1])**2 + (state1[0] - state2[0])**2 )**(0.5)

	return M_distance + L_distance

# Sort the states based on heuristic value (Ascending)
def selection_sort_states_byHeuristic(states):
	i = 0
	j = 0

	sorted_states = list()

	for X in states:
		smallest = copy.deepcopy(X)
		exchange = False
		for Y in states[i+1:] :
			if Y[2] <= smallest[2]:
				smallest = copy.deepcopy(Y)
				small_loc = j + i + 1
				exchange = True
			j = j + 1
		
		if exchange:
			states[small_loc] = copy.deepcopy(states[i])
			states[i] = copy.deepcopy(smallest)

		i = i + 1
		j = 0

# Merge two sorted states lists based on heuristic value (Ascending)
def Merge_two_states_lists(listX, listY):
	X_ind = 0
	Y_ind = 0

	Max_X_ind = len(listX) - 1
	Max_Y_ind = len(listY) - 1

	merged_list = list()

	while (X_ind <= Max_X_ind and Y_ind <= Max_Y_ind):
		if listX[X_ind][2] < listY[Max_Y_ind][2]:
			merged_list.append(listX[X_ind])
			X_ind = X_ind + 1
		elif listX[X_ind][2] > listY[Y_ind][2]:
			merged_list.append(listY[Y_ind])
			Y_ind = Y_ind + 1
		else:
			merged_list.append(listY[Y_ind])
			merged_list.append(listX[X_ind])
			X_ind = X_ind + 1
			Y_ind = Y_ind + 1

	while X_ind <= Max_X_ind:
		merged_list.append(listX[X_ind])
		X_ind = X_ind + 1

	while Y_ind <= Max_Y_ind:
		merged_list.append(listY[Y_ind])
		Y_ind = Y_ind + 1

	return merged_list

# Generate the next possible paths
def Next_State_Generator(maze, current_location, goal_location, visited_locations):

	max_vertical = len(maze) - 1
	max_horizontal = len(maze[0]) - 1

	allowed_location_1 = None
	allowed_location_2 = None
	allowed_location_3 = None
	allowed_location_4 = None
	next_states = list()

	# UP
	# Check if UP location is inside the maze
	if(current_location[0] - 1 >= 0):
		# Check if it is possible to move UP
		if(maze[current_location[0] - 1] [current_location[1]] == free_tile):
			# check if the path was already visited
			if([current_location[0] - 1, current_location[1]] not in visited_locations):
				allowed_location_1 = [current_location[0] - 1, current_location[1], Heuristic_calc(goal_location, [current_location[0] - 1, current_location[1]])]
				next_states.append(allowed_location_1)

	# DOWN
	# Check if DOWN location is inside the maze
	if (current_location[0] + 1 <= max_vertical):
		# Check if it is possible to move DOWN
		if(maze[current_location[0] + 1] [current_location[1]] == free_tile):
			# check if the path was already visited
			if([current_location[0] + 1, current_location[1]] not in visited_locations):
				allowed_location_2 = [current_location[0] + 1, current_location[1], Heuristic_calc(goal_location, [current_location[0] + 1, current_location[1]])]
				next_states.append(allowed_location_2)
	#LEFT
	# Check if LEFT location is inside the maze
	if(current_location[1] - 1 >= 0):
		# Check if it is possible to move LEFT
		if(maze[current_location[0]] [current_location[1] - 1] == free_tile):
			# check if the path was already visited
			if([current_location[0], current_location[1] - 1] not in visited_locations):
				allowed_location_3 = [current_location[0], current_location[1] - 1, Heuristic_calc(goal_location, [current_location[0], current_location[1] - 1])]
				next_states.append(allowed_location_3)
	#RIGHT
	# Check if RIGHT location is inside the maze
	if(current_location[1] + 1 <= max_horizontal):
		# Check if it is possible to move RIGHT
		if(maze[current_location[0]] [current_location[1] + 1] == free_tile):
			# check if the path was already visited
			if([current_location[0], current_location[1] + 1] not in visited_locations):
				allowed_location_4 = [current_location[0], current_location[1] + 1, Heuristic_calc(goal_location, [current_location[0], current_location[1] + 1])]
				next_states.append(allowed_location_4)
	
	# Sort it
	selection_sort_states_byHeuristic(next_states)
	traceX(ACT, str(next_states))
	return next_states

# Print the solution to a .txt file
def Create_Solution_Map(maze, path_trace):
	#fileP = open("Maze_solution.txt", 'w')
	fileP = codecs.open(soln_file_loc, mode="w", encoding="utf16")
	maze_string = str()

	# Logic to place arrows in map
	i = 0
	for loc in path_trace:
		if(i != len(path_trace) - 1):
			if(loc[0] > path_trace[i+1][0]):
				maze[loc[0]][loc[1]] = up_arrow

			if(loc[0] < path_trace[i+1][0]):
				maze[loc[0]][loc[1]] = down_arrow

			if(loc[1] > path_trace[i+1][1]):
				maze[loc[0]][loc[1]] = left_arrow

			if(loc[1] < path_trace[i+1][1]):
				maze[loc[0]][loc[1]] = right_arrow

		i = i + 1

	# Create a string to write into the file
	for lineX in maze:
		for charX in lineX:
			maze_string = maze_string + charX

	fileP.write('Solution :\n' + Extra_Text + '\n' + Author + maze_string + '\n\nFull Path - \n' + str(path_trace))

	im= Image.new('RGB', (len(maze[0]), len(maze)))

	i = 0
	j = 0
	ij = tuple()
	for rowX in range(len(maze[0]) - 1):
		for pxl in range(len(maze)):
			ij = (i,j)
			if(maze[j][i] == blocked_tile):
				im.putpixel(ij,(0,0,0))
			elif(maze[j][i] == free_tile):
				im.putpixel(ij,(255,255,255))
			else:
				im.putpixel(ij,(255,0,0))
			j = j + 1

		i = i + 1
		j = 0

	im.save('solution.jpg')

#down_arrow = 'v'
#up_arrow = '^'
#left_arrow = '<'
#right_arrow = '>'

# Unicode characters (Arrows) to print into .txt file 
down_arrow = '\u25BC'
up_arrow = '\u25B2'
left_arrow = '\u25C4'
right_arrow = '\u25BA'

regular_maze = True
maze = list()
maze_file = None

try:
	# Open the Maze file (File where the maze is located)
	maze_file = open(maze_file_loc, 'r')

	for lineX in maze_file:
			lineX = list(lineX)
			maze.append(lineX)
except:
	print("Some issue with Maze.txt file\nEnsure (Maze.txt) the file is present and readable")

# Run the path finding algorithm only if the maze file is proper
if len(maze) != 0 and maze_file and regular_maze:

	# Format of a state:
	# [vertical location, horizontal location,  Heuristic value of the location]

	#initialize with some value, say 0
	start_i = 0
	start_j = 0
	goal_i = 0
	goal_j = 0


	i = 0
	j = 0
	found1 = False
	found2 = False
	# Logic to find the start location
	for maze_lineX in maze:
		for maze_char in maze_lineX:
			# Search for 'S'
			if maze_char == 'S':
				start_i = i
				start_j = j
				found1 = True
			j = j + 1
		i = i + 1
		j = 0

		if found1:
			break

	i = 0
	j = 0
	found = False
	# Logic to find the goal location
	for maze_lineX in maze:
		for maze_char in maze_lineX:
			# Search for 'G'
			if maze_char == 'G':
				goal_i = i
				goal_j = j
				found2 = True
			j = j + 1
		i = i + 1
		j = 0

		if found2:
			break

	# Run the algorithm only if Start and goal states are found
	if found2 and found1:
		goal_location = [goal_i,goal_j, 0]
		start_location = [start_i,start_j]
		# make the goal location a free tile (To ensure the algorithm does not treat it as a blocked location)
		maze[goal_i][goal_j] = free_tile
		maze[start_i][start_j] = free_tile

		start_location = start_location + [Heuristic_calc(start_location, goal_location)]
		current_location = start_location
		available_location = list()
		next_Locations = list()
		visited_locations = list()
		traceBack_dict = {'START':current_location[0:2]}
		path_trace = list()
		Number_Of_iterations = 0

		print('Start Location - ' + str(start_location))
		print('Goal Location - ' + str(goal_location) + '\n')

		next_Locations = Next_State_Generator(maze, current_location, goal_location, visited_locations)
		available_location = copy.deepcopy(next_Locations)
		visited_locations.append(current_location[0:2])
		for locationX in next_Locations:
			traceBack_dict.update({str(locationX[0:2]):current_location[0:2]})


		while available_location and current_location != goal_location:
			# Perform a best first search 
			# (First location in available_location contains element with least heuristic value)
			current_location = available_location[0]
			available_location = available_location[1:]
			next_Locations = Next_State_Generator(maze, current_location, goal_location, visited_locations)

			for locationX in next_Locations:
				traceBack_dict.update({str(locationX[0:2]):current_location[0:2]})

			available_location = Merge_two_states_lists(next_Locations, available_location)
			#add 1 to this values

			visited_locations.append(current_location[0:2])
			Number_Of_iterations = Number_Of_iterations + 1


		if current_location == goal_location:
			# Logic to recreate the solution path
			while current_location != start_location[0:2]:
				path_trace.append(current_location[0:2])
				current_location = traceBack_dict[str(current_location[0:2])]

			path_trace = path_trace + [start_location[0:2]]
			path_trace.reverse()
			print('Path = ' + str(path_trace))
			Extra_Text = '\nNumber of iterations = ' + str(Number_Of_iterations) + '\nPath length = ' + str(len(path_trace)) + '\nA* Efficiency = ' + str((len(path_trace)/Number_Of_iterations) * 100)
			Create_Solution_Map(maze, path_trace)

			#Print statistics of the algorithm
			print('\nNumber of iterations = ' + str(Number_Of_iterations))
			print('Path length = ' + str(len(path_trace)))
			print('A* Efficiency = ' + str((len(path_trace)/Number_Of_iterations) * 100))

		else:
			print('No path Found - ' + str(Number_Of_iterations))