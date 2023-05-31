import sys
import percept
import random
random.seed(42)

class init_world:
    
    def __init__(self):
        grid_size = 6
        self.world = [[0] * grid_size for _ in range(grid_size)]
        # danger prob - 계산 : [safe] = 0 추론 -> safe -> 0
        self.danger_prob = [[[1,1] for x in range(6)] for y in range(6)]   # 초기 세팅 = 1, 벽은 -1 [0] : wumpus, [1]: pitch
        
        # Set up walls around the grid
        for i in range(grid_size):
            self.world[0][i] = 1    # top wall
            self.world[grid_size-1][i] = 1    # bottom wall
            self.world[i][0] = 1    # left wall
            self.world[i][grid_size-1] = 1    # right wall
            
            self.danger_prob[0][i] = False    # top wall
            self.danger_prob[grid_size-1][i] = False    # bottom wall
            self.danger_prob[i][0] = False    # left wall
            self.danger_prob[i][grid_size-1] = False    # right wall
        
        # # Print the self.world
        # for row in self.world:
        #     print(row)
        
        init_state = {'breeze': False, 'stench': False, 'glitter': False, 'scream': False, 'bump': True}
        self.state_grid = [[{key: value for key, value in init_state.items()} for _ in range(6)] for _ in range(6)]
        
        
        # Set the wumpus and pit probability
        prob = 0.1
        gold_x = random.randint(1,3)
        gold_y = random.randint(2,4)
        print(gold_x, gold_y)
        self.state_grid[gold_x][gold_y]['glitter'] = True
        self.world[gold_x][gold_y] = 'G'
        
        # Generate wumpus and pit with probability 0.1 for each cell except (1,1)
        for i in range(1, 5):
            for j in range(1, 5):
                self.state_grid[i][j]['bump'] = False # 벽이 아닌 부분 bump False로 바꿈
                if (i, j) != (4, 1) and self.world[i][j] != 'G' and random.random() < prob:
                    self.world[i][j] = "W"
                    self.state_grid[i][j]['stench'] = True
                    self.state_grid[i+1][j]['stench'] = True
                    self.state_grid[i][j+1]['stench'] = True
                    self.state_grid[i-1][j]['stench'] = True
                    self.state_grid[i][j-1]['stench'] = True
                    continue
              
                if (i, j) != (4, 1) and self.world[i][j] != 'G' and random.random() < prob:
                    self.world[i][j] = "P"
                    self.state_grid[i][j]['breeze'] = True
                    self.state_grid[i+1][j]['breeze'] = True
                    self.state_grid[i][j+1]['breeze'] = True
                    self.state_grid[i-1][j]['breeze'] = True
                    self.state_grid[i][j-1]['breeze'] = True
                
                
                        
        for row in self.world:
            print(row)
        
        
        # agent 위치정보 따로 저장 [4,1]
        self.agent = {'xy': [4, 1], 'dir': 'East', 'arrow': 2,'isgrab':False}
        
        
        # visited - 방문 한 것 저장
        self.visited = [[0 for x in range(6)] for y in range(6)]
       
        
        
        # KB : wumpus 추론 logic => 결과 저장. : stench, breeze 정보 저장
        self.caution_grid = {'stench':set(),'breeze':set()}
        
        
        # Print the self.world
        print('\n')

        for row in self.danger_prob:
            print(row)
            
    
    def update_visited(self, x, y):
        self.visited[x][y] = 1
        self.update_danger_prob(x,y)
        return self.visited
    
    
    def KB(self,x,y,env): # stench = 0, breeze = 1
        c = []
        dx = [1,-1,0,0]
        dy = [0,0,1,-1]
            
        for i in range(4):
            nx = x + dx[i]
            ny = y + dy[i]
            if nx > 4 or nx < 1 or ny > 4 or ny < 1:
                continue
            
            if self.danger_prob[nx][ny][env] != 0:
                c.append([nx, ny])
        print(c)            
        if len(c) == 1: # 오직 하나만 0이 아닐 경우,
            xy = c.pop()
            self.danger_prob[xy[0]][xy[1]][env] = 100
            self.danger_prob[xy[0]][xy[1]][env^1] = 0
        
        
        
    
 

    def update_danger_prob(self, x, y):
        # 현재 위치에 대해서 확인
        if self.world[x][y] == 'W':
            self.danger_prob[x][y][0] = 100
            self.danger_prob[x][y][1] = 0  # and die
            return self.danger_prob
        
        elif self.world[x][y] == 'P': 
            self.danger_prob[x][y][1] = 100 
            self.danger_prob[x][y][0] = 0  # and die
            return self.danger_prob
        else:
            self.danger_prob[x][y] = [0,0]
         
        # stench나 breeze를 느꼈을 경우 해당 그리드 추가
        if percept.sense_stench(self) == True:
            self.caution_grid['stench'].add((x,y))
        if percept.sense_breeze(self) == True:
            self.caution_grid['breeze'].add((x,y))
            
        # 주변 그리드에 대해서
        
        dx = [1,-1,0,0]
        dy = [0,0,1,-1]
        
        
            
            
        for i in range(4):
            nx = x + dx[i]
            ny = y + dy[i]
            if nx > 4 or nx < 1 or ny > 4 or ny < 1:
                continue
            if percept.sense_stench(self) == False: # stench를 느끼지 못했을 경우
                self.danger_prob[nx][ny][0] = 0    # 주위 칸 0으로 바꿈.
            if percept.sense_breeze(self) == False: #  breeze를 느끼지 못했을 경우
                self.danger_prob[nx][ny][1] = 0    # 주위 칸 0으로 바꿈
            
            # stench나 breeze를 느꼈을 경우
                
            if self.danger_prob[nx][ny][0] != 0 and  self.danger_prob[nx][ny][0] != 100:  # wumpus가 없는게 확실하다면 0, wumpus가 있는게 확실하다면 100 
                self.danger_prob[nx][ny][0] += 1
            if self.danger_prob[nx][ny][1] != 0 and  self.danger_prob[nx][ny][1] != 100:  # wumpus가 없는게 확실하다면 0, wumpus가 있는게 확실하다면 100 
                self.danger_prob[nx][ny][1] += 1
            
        
        # stench나 breeze가 있는 그리드의 주변 그리드에 대해 KB계산
        print(self.caution_grid)
        for _,env in enumerate(self.caution_grid):
            for g in self.caution_grid[env]:
                self.KB(g[0],g[1],env = _)
               
        
        
        
        return self.danger_prob
    
   
    
    # stench가 shoot 당한 wumpus가 아니라 다른 wumpus에 의해 생긴 경우 재로드                
    def update_state_grid(self,x, y):
        self.wumpus_list = list()
        if x-2 > -1 and x+2 < 6 and y-2 > -1 and y+2 <6:
            self.find_wumpus(x-2,y)
            self.find_wumpus(x+2,y)
            self.find_wumpus(x,y-2)
            self.find_wumpus(x,y+2)
        
        self.find_wumpus(x-1,y-1)
        self.find_wumpus(x-1,y+1)
        self.find_wumpus(x+1,y-1)
        self.find_wumpus(x+1,y+1)
        
        
        for i in range(len(self.wumpus_list)):

            x = self.wumpus_list[i][0]
            y = self.wumpus_list[i][1]
            self.set_stench(x,y)      
        
        return self.state_grid
    
    def find_wumpus(self, x, y):
        if self.world[x][y] == "W":
            self.wumpus_list.append([x,y])
        else:
            return 0
        
    def set_stench(self, i, j):
        self.state_grid[i][j]['stench'] = True
        self.state_grid[i+1][j]['stench'] = True
        self.state_grid[i][j+1]['stench'] = True
        self.state_grid[i-1][j]['stench'] = True
        self.state_grid[i][j-1]['stench'] = True
    
    
    def update_agent(self, xy= False, direct = False, arrow = False, isgrab = False):
        if xy:
            self.agent['xy'] = xy
        if direct:
            self.agent['dir'] = direct
        if arrow:
            self.agent['arrow'] = arrow
        if isgrab:
            self.agent['isgrab'] = True

        return self.agent
    

# main 함수 구현

def main():
    # Create an instance of the init_world class
    # init_world()
    world = init_world()
    
    # Perform operations on the world instance
    # For example, you can access the agent's location and print it
    
    # update_agent test
    
    agent = world.agent
    world.update_agent(direct = 'North')
    
    print("Agent's location:", agent)
    
    # update_world and update state_grid test
    world1 = world.world
    world.update_world(x = 1, y = 1)
    print(world1[1][1])
    for row in world1:
        print(row)
    print("State in (1,1) : ", world.state_grid[1][1])
    print("State in (4,1) : ", world.state_grid[4][1])
    # update_visited test
    
    visit = world.visited
    danger = world.danger_prob

    x = agent['xy'][0]
    y = agent['xy'][1]
    world.update_visited(x, y)  # agent 현재 위치
    
    print("visited")
    for row in visit:
        print(row)
    
    print("danger")
    for row in danger:
        print(row)
    print("\n")   
    # update_danger_prob test
    world.update_agent(xy = [4,2])
    
    x = agent['xy'][0]
    y = agent['xy'][1]
    world.update_visited(x, y)
    
    print("visited2")
    for row in visit:
        print(row)
    
    print("danger2")
    for row in danger:
        print(row)
    
    print("\n")
    # update_danger_prob test2
    world.update_agent(xy = [4,3])
    
    x = agent['xy'][0]
    y = agent['xy'][1]
    world.update_visited(x, y)
    
    print("visited3")
    for row in visit:
        print(row)
    
    print("danger3")
    for row in danger:
        print(row)
    print("\n")
    # update_danger_prob test3
    world.update_agent(xy = [2,2])
    
    x = agent['xy'][0]
    y = agent['xy'][1]
    world.update_visited(x, y)
    
    print("visited3")
    for row in visit:
        print(row)
    
    print("danger3")
    for row in danger:
        print(row)
    
    
    
# Call the main function
if __name__ == "__main__":
    main()
      
        

