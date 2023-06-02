import percept

from collections import deque

def bfs_visited(self, start, end):
    # Define the directions: up, down, left, right
    directions = [(1, 0), (-1, 0), (0, 1), (0, -1)]

    # Get the grid size
    rows = len(self.danger_prob)
    cols = len(self.danger_prob[0])

    # Create a visited array to keep track of visited cells
    visited = [[False for _ in range(cols)] for _ in range(rows)]

    # Create a parent array to store the parent cell for each visited cell
    parent = [[None for _ in range(cols)] for _ in range(rows)]

    # Create a queue for BFS traversal
    queue = deque()

    # Add the start cell to the queue and mark it as visited
    queue.append(start)
    visited[start[0]][start[1]] = True

    # Perform BFS
    while queue:
        curr_x, curr_y = queue.popleft()

        # Check if we reached the destination
        if (curr_x, curr_y) == end:
            # Build the path from end to start using parent information
            path = []
            curr = end
            while curr != start:
                path.append(curr)
                curr = parent[curr[0]][curr[1]]
            path.append(start)
            path.reverse()
            return path

        # Explore the neighbors
        for dx, dy in directions:
            new_x = curr_x + dx
            new_y = curr_y + dy

            # Check if the neighbor is within the grid bounds and is a valid path
            if 0 <= new_x < rows and 0 <= new_y < cols and self.danger_prob[new_x][new_y] == [0,0] and not visited[new_x][new_y]:
                queue.append((new_x, new_y))
                visited[new_x][new_y] = True
                parent[new_x][new_y] = (curr_x, curr_y)

    # If the destination is not reachable, return an empty path
    return []

def find_direction(self, start, end):
    dx, dy = end[0] - start[0], end[1] - start[1]
    if dx == 0 and dy == 1:
        return 'East'
    elif dx == 0 and dy == -1:
        return 'West'
    elif dx == 1 and dy == 0:
        return 'South'
    elif dx == -1 and dy == 0:
        return 'North'
    else:
        raise ValueError("Invalid cells for finding direction")

def move_in_direction(self, diection):
    if self.agent['dir'] != diection:
        if ((self.agent['dir'] == 'East' and dir == 'South') or
            (self.agent['dir'] == 'South' and dir == 'West') or
            (self.agent['dir'] == 'West' and dir == 'North') or
            (self.agent['dir'] == 'North' and dir == 'East')):
            turnRight(self)
        else:
            turnLeft(self)
    goForward(self)

def goBackToStartVisited(self):
    path = bfs_visited(self,tuple(self.agent['xy']), (4,1))
    print('path: ', path)
    for i in range(len(path) - 1):
        direction = find_direction(self,path[i], path[i+1])
        move_in_direction(self,direction)

def die(self):
    self.agent = {'xy': [4, 1], 'dir': 'East', 'arrow': 2,'isgrab':False}
    return "Die"


# define each actions
def goForward(self):
    ag_x = self.agent['xy'][0]
    ag_y = self.agent['xy'][1]
    dir = self.agent['dir']
    
    if dir == "East":
        ag_y+=1
    elif dir == "West":
        ag_y-=1
    elif dir == "North":
        ag_x-=1
    elif dir == "South":
        ag_x+=1
    

    return [ag_x, ag_y]


def turnLeft(self):
    dir = self.agent['dir']

    if dir == "East":
        dir = "North"
    elif dir == "West":
        dir = "South"
    elif dir == "North":
        dir = "West"
    elif dir == "South":
        dir = "East"
    
    self.agent['dir'] = dir
    
    return "turnLeft"


def turnRight(self):
    dir = self.agent['dir']

    if dir == "East":
        dir = "South"
    elif dir == "West":
        dir = "North"
    elif dir == "North":
        dir = "East"
    elif dir == "South":
        dir = "West"

    self.agent['dir'] = dir

    return "turnRight"


def shoot(self):
    x = self.agent['xy'][0]
    y = self.agent['xy'][1]
    dir = self.agent['dir']

    
    self.agent['arrow']-=1
    # search wumpus in row that agent exists. If it exists, shoot 
    if dir == "East": 
        for n in range(y, 5):
            self.danger_prob[x][n][0] = 0
            if(self.world[x][n] == "W"):
                self.world[x][n] = 0
                self.state_grid[x][n]['stench'] = False
                self.state_grid[x+1][n]['stench'] = False
                self.state_grid[x][n+1]['stench'] = False
                self.state_grid[x-1][n]['stench'] = False
                self.state_grid[x][n-1]['stench'] = False

                self.update_state_grid(x, n)
                return "Scream"
    elif dir == "West":
        for n in range(y, 1, -1):
            self.danger_prob[x][n][0] = 0
            if(self.world[x][n] == "W"):
                self.world[x][n] = 0
                self.state_grid[x][n]['stench'] = False
                self.state_grid[x+1][n]['stench'] = False
                self.state_grid[x][n+1]['stench'] = False
                self.state_grid[x-1][n]['stench'] = False
                self.state_grid[x][n-1]['stench'] = False

                self.update_state_grid(x, n)
                return "Scream"
    elif dir == "North":
        for m in range(x, 1, -1):
            self.danger_prob[m][y][0] = 0
            if(self.world[m][y] == "W"):
                self.world[m][y] = 0
                self.state_grid[m][y]['stench'] = False
                self.state_grid[m+1][y]['stench'] = False
                self.state_grid[m][y+1]['stench'] = False
                self.state_grid[m-1][y]['stench'] = False
                self.state_grid[m][y-1]['stench'] = False

                self.update_state_grid(m, y)
                return "Scream"    
    elif dir == "South":
        for m in range(x, 5):
            self.danger_prob[m][y][0] = 0
            if(self.world[m][y] == "W"):
                self.world[m][y] = 0
                self.state_grid[m][y]['stench'] = False
                self.state_grid[m+1][y]['stench'] = False
                self.state_grid[m][y+1]['stench'] = False
                self.state_grid[m-1][y]['stench'] = False
                self.state_grid[m][y-1]['stench'] = False

                self.update_state_grid(m, y)
                return "Scream"    
    
    return 0    


def grab(self):
    x = self.agent['xy'][0]
    y = self.agent['xy'][1]

    if self.agent['isgrab'] == False and self.world[x][y] == 'G':
        self.agent['isgrab'] = True
        self.state_grid[x][y]['glitter'] = False
    goBackToStartVisited(self)

    return "Grab"

def climb(self):
    return "Climb"

turn = 0

# details for when do each action do
def reasoning(self):
    dir = self.agent['dir']
    
    if self.agent['isgrab'] and self.agent['xy'] == [4,1]:
        return [climb(self)]
    elif percept.sense_glitter(self):
        return [grab(self)]
    else:
        before_x = self.agent['xy'][0]
        before_y = self.agent['xy'][1]
        ag_pos = goForward(self)
        after_x = ag_pos[0]
        after_y = ag_pos[1]

        
        if self.world[before_x][before_y] == "W" or self.world[before_x][before_y] == "P":
            return [die(self)]
        elif percept.sense_bump(self, after_x, after_y):
            print(self.agent['dir'])
            for row in self.state_grid:
                print(row)
            self.update_visited(after_x, after_y)
            if dir == "East" :
                if percept.sense_bump(self, after_x+1, after_y):
                    return ["Bump", turnRight(self)]
            elif dir == "West":
                if percept.sense_bump(self, after_x-1, after_y):
                    return ["Bump", turnRight(self)]
            elif dir == "North":
                if percept.sense_bump(self, after_x, after_y-1):
                    return ["Bump", turnRight(self)]
            elif dir == "South":
                if percept.sense_bump(self, after_x, after_y+1):
                    return ["Bump", turnRight(self)]
            return ["Bump", turnLeft(self)]
        
        elif percept.sense_bump(self, after_x, after_y) == False: # if the node, agent want to go, is wall, don't move
            print(self.agent['arrow'])
            neighbors = [(before_x+i, before_y+j) for i, j in [[0, 1], [-1, 0], [0, -1], [1, 0]] if before_x+i > 0 and before_x+i < 5 and before_y+j >0 and before_y+j < 5]
            direction = ['East','North','West','South'] # 방향 
            for i, j in neighbors:
                if self.danger_prob[i][j][0] == 100:
                    g_n = (i, j)
                    p_d = direction.index(self.agent['dir'])
                    g_d = neighbors.index(g_n)
                    itr = p_d - g_d
                    for _ in range(abs(itr)):
                        if  itr < 0: # turn left
                            turnLeft(self)
                                
                        elif itr > 0: # turn right
                            turnRight(self)
                        else:
                            break
            print(self.agent['dir'])
            ag_pos = goForward(self)
            after_x = ag_pos[0]
            after_y = ag_pos[1]      

            if self.danger_prob[after_x][after_y][0] > 1 and self.agent['arrow'] > 0:
                print(self.agent)
                return ["Shoot", percept.sense_scream(self)]
            elif self.danger_prob[after_x][after_y][1] > 1:
                print(self.agent['dir'])
            # if dir == "East" :
            #     return ["Danger", self.turnRight(self)]
            # elif dir == "West":
            #     return ["Danger", self.turnRight(self)]
            # elif dir == "North":
            #     return ["Danger", self.turnRight(self)]
            # elif dir == "South":
            #     return ["Danger", self.turnRight(self)]
                return ["Danger", turnLeft(self)]
            else:
                # self.update_danger_prob()
                self.agent['xy'] = [after_x, after_y]
                self.update_visited(after_x, after_y)
                return ["GoForward", dir, percept.sense_breeze(self), percept.sense_stench(self)]
        
        

        


    

