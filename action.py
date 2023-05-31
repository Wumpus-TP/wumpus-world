import percept

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

    if self.agent['isGrab'] == False and self.world[x][y] == 'G':
        self.agent['isGrab'] = True
        self.state_grid[x][y]['glitter'] = False

    return "Grab"

def climb(self):
    return "Climb"

turn = 0

# details for when do each action do
def reasoning(self):
    dir = self.agent['dir']
    
    if self.agent['isgrab'] and self.agent['xy'] == [4, 1]:
        return [climb(self)]
    elif percept.sense_glitter(self):
        return [grab(self)]
    else:
        before_x = self.agent['xy'][0]
        before_y = self.agent['xy'][1]
        ag_pos = goForward(self)
        after_x = ag_pos[0]
        after_y = ag_pos[1]

        # agent가 괴물이나 웅덩이를 마주쳤을 때의 행동
        if self.world[before_x][before_y] == "W" or self.world[before_x][before_y] == "P":
            return [die(self)]
        
        # agent가 이동할 최적의 이동 경로
        if [after_x, after_y] not in self.visited[after_x]:
            if ([before_x+1, before_y] in self.visited[before_x+1] and
                self.danger_prob[before_x+1][before_y] == [0,0]):
                self.agent['xy'] = [before_x+1,before_y]
                self.update_visited(before_x+1,before_y)
                return ["BestWay", dir, "South"]
            elif ([before_x, before_y+1] in self.visited[before_x] and
                self.danger_prob[before_x][before_y+1] == [0,0]):
                self.agent['xy'] = [before_x,before_y+1]
                self.update_visited(before_x,before_y+1)
                return ["BestWay", dir, "East"]
            elif ([before_x-1, before_y] in self.visited[before_x-1] and
                self.danger_prob[before_x-1][before_y] == [0,0]):
                self.agent['xy'] = [before_x-1,before_y]
                self.update_visited(before_x-1,before_y)
                return ["BestWay", dir, "North"]
            elif ([before_x, before_y-1] in self.visited[before_x] and
                self.danger_prob[before_x][before_y-1] == [0,0]):
                self.agent['xy'] = [before_x,before_y-1]
                self.update_visited(before_x,before_y-1)
                return ["BestWay",dir, "West"]

        # agent가 벽에 부딪혔을 때의 이동
        if percept.sense_bump(self, after_x, after_y):
            print(self.agent['dir'])
            del(self.visited[after_x][after_y])
            if dir == "East":
                if ([after_x-1, after_y] not in self.visited[after_x-1]
                    and percept.sense_bump(self, after_x-1, after_y)):
                    return ["Bump", turnRight(self)]
            elif dir == "West":
                if ([after_x+1, after_y] not in self.visited[after_x+1]
                    and percept.sense_bump(self, after_x+1, after_y)):
                    return ["Bump", turnRight(self)]
            elif dir == "North":
                if ([after_x, after_y-1] not in self.visited[after_x]
                    and percept.sense_bump(self, after_x, after_y-1)):
                    return ["Bump", turnRight(self)]
            elif dir == "South":
                if ([after_x, after_y+1] not in self.visited[after_x]
                    and percept.sense_bump(self, after_x, after_y+1)):
                    return ["Bump", turnRight(self)]
            return ["Bump", turnLeft(self)]
        
        elif percept.sense_bump(self, after_x, after_y) == False: # if the node, agent want to go, is wall, don't move
            print(self.agent['arrow'])
            # agent가 위험을 감지했을 때의 행동
            if [after_x, after_y] in self.visited[after_x]:
                if self.danger_prob[after_x][after_y][0] > 1 and self.agent['arrow'] > 0:
                    return ["Shoot", percept.sense_scream(self)]
                elif self.danger_prob[after_x][after_y][1] > 1:
                    return ["Danger", turnLeft(self)]
            # agent의 기본 행동
            self.agent['xy'] = [after_x, after_y]
            self.update_visited(after_x, after_y)
            return ["GoForward", dir, percept.sense_breeze(self), percept.sense_stench(self)]
    
        

        


    

