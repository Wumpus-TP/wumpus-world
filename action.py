import percept
import heapq
# import SetWorld as self

# if agent die, reset agent's state
def die(self):
    self.agent = {'xy': [4, 1], 'dir': 'East', 'arrow': 2,'isgrab':False}
    self.update_visited(4, 1)
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
                self.danger_prob[x][n][1] = 0
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
                self.danger_prob[x][n][1] = 0
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
                self.danger_prob[m][y][1] = 0
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
                self.danger_prob[m][y][1] = 0
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

    return "Grab"

def climb(self):
    return "Climb"

# 현재 위치에서 원하는 위치의 격자까지의 비용 계산 클래스
class Grid:
    def __init__(self, state, parent=None, g=0, h=0, f=0):
        self.state = state
        self.parent = parent
        self.g = g  # g(n): 비용
        self.h = h  # h(n): 휴리스틱 함수 값
        self.f = f

    def __lt__(self, other):
        return self.state == other.state

# 원하는 위치의 격자에 접근하기 위한 함수
def find_path(self, start, sum_danger, get_neighbors_func, isgrab):
    goal = (4, 1) # 다시 돌아가야 할 노드
    
    open_list = []
    closed_list = set()
    path_costs = {}  # 각 노드까지의 최적 비용을 저장하기 위한 딕셔너리
    danger_heur = {} # 각 노드의 위험확률을 저장하기 위한 딕셔너리

    # 시작 노드 초기화
    start_node = Grid(start, g=0, h=0)
    heapq.heappush(open_list, start_node)
    path_costs[start] = 0

    while open_list:
        current_node = heapq.heappop(open_list)

        # 금을 획득하면,
        # 다시 원래 자리로 돌아가야하므로 시작 지점까지 가는 루트 탐색
        if isgrab == True and current_node.state == goal:
            return end_to_start(self, current_node)

        if current_node.state in closed_list:
            continue

        closed_list.add(current_node.state)

        neighbors = []
        neighbors = get_neighbors_func(current_node.state)
        
        for neighbor_state in neighbors:
            if isgrab == True:
                if [neighbor_state[0], neighbor_state[1]] in self.visited:
                    neighbor_g = current_node.g + 1  # 비용은 항상 1로 가정
                    neighbor_h = ((current_node.state[0] - neighbor_state[0]) ** 2) + ((current_node.state[1] - neighbor_state[1]) ** 2)
                    neighbor_node = Grid(neighbor_state, parent=current_node, g=neighbor_g, h=neighbor_h, f=neighbor_g + neighbor_h)
                    
                    if neighbor_state not in path_costs or neighbor_g < path_costs[neighbor_state]:
                        path_costs[neighbor_state] = neighbor_g
                        danger_heur[neighbor_state] = sum_danger(self, neighbor_state)
                        heapq.heappush(open_list, neighbor_node)
            else:
                neighbor_g = current_node.g + 1  # 비용은 항상 1로 가정
                neighbor_h = ((current_node.state[0] - neighbor_state[0]) ** 2) + ((current_node.state[1] - neighbor_state[1]) ** 2)
                neighbor_node = Grid(neighbor_state, parent=current_node, g=neighbor_g, h=neighbor_h, f=neighbor_g + neighbor_h)

                if neighbor_state not in path_costs or neighbor_g < path_costs[neighbor_state]:
                    path_costs[neighbor_state] = neighbor_g
                    danger_heur[neighbor_state] = sum_danger(self, neighbor_state)
                    heapq.heappush(open_list, neighbor_node)

    return [path_costs,sorted(danger_heur.items(), key=lambda x:x[1])]

# 휴리스틱 함수 = wumpus가 있을 확률+ pitch가 있을 확률
def sum_danger(self, state):
    heuristic = self.danger_prob[state[0]][state[1]][0] + self.danger_prob[state[0]][state[1]][1]
    return heuristic

# 현재 노드와 연결된 인접한 노드들을 반환, 근처에 벽이 있으면 노드 출력 x
def get_neighbors_func(state):
    neighbors = []
    row, col = state
    if row > 1:
        neighbors.append((row-1, col))  # 상
    if row < 4:
        neighbors.append((row+1, col))  # 하
    if col > 1:
        neighbors.append((row, col-1))  # 좌
    if col < 4:
        neighbors.append((row, col+1))  # 우
    return neighbors

# 방문했던 노드를 기준으로 다시 돌아가는 루트 탐색
def end_to_start(self, current_node):
    path = []
    while current_node:
        path.append(current_node.state)
        current_node = current_node.parent
    return path 


# details for when do each action do
def reasoning(self):

    dir = self.agent['dir']
    before_x = self.agent['xy'][0]
    before_y = self.agent['xy'][1]
    
    if percept.sense_glitter(self):
        self.world[before_x][before_y] = 0
        path = find_path(self, (before_x, before_y), sum_danger, get_neighbors_func, True)
        print(path)
        return [grab(self), path]
    else:
        ag_pos = goForward(self)
        after_x = ag_pos[0]
        after_y = ag_pos[1]

        # agent가 괴물이나 웅덩이를 마주쳤을 때의 행동
        if self.world[before_x][before_y] == "W" or self.world[before_x][before_y] == "P":
            self.visited.remove([before_x, before_y])
            return [die(self)]
        
        # agent가 벽에 부딪혔을 때의 이동
        if percept.sense_bump(self, after_x, after_y):
            print(self.agent['dir'])
            if dir == "East":
                if ([after_x-1, after_y] in self.visited
                    and percept.sense_bump(self, after_x-1, after_y)):
                    return ["Bump", turnRight(self)]
            elif dir == "West":
                if ([after_x+1, after_y] in self.visited
                    and percept.sense_bump(self, after_x+1, after_y)):
                    return ["Bump", turnRight(self)]
            elif dir == "North":
                if ([after_x, after_y-1] in self.visited
                    and percept.sense_bump(self, after_x, after_y-1)):
                    return ["Bump", turnRight(self)]
            elif dir == "South":
                if ([after_x, after_y+1] in self.visited
                    and percept.sense_bump(self, after_x, after_y+1)):
                    return ["Bump", turnRight(self)]
            return ["Bump", turnLeft(self)]
        
        elif percept.sense_bump(self, after_x, after_y) == False: # if the node, agent want to go, is wall, don't move
            print(self.agent['arrow'])
            # agent가 위험을 감지했을 때의 행동
            if [after_x, after_y] not in self.visited:
                if self.danger_prob[after_x][after_y][0] > 1 and self.agent['arrow'] > 0:
                    return ["Shoot", percept.sense_scream(self)]
                elif self.danger_prob[after_x][after_y][1] > 1:
                    return ["Danger", turnLeft(self)]
                
            # agent가 이동할 최적의 이동 경로
            elif [after_x, after_y] in self.visited:
                result = find_path(self, (before_x, before_y), sum_danger, get_neighbors_func, False)
                path_costs = result[0]
                danger_heur = result[1]
                min_visit = [None, 5]
                for pos, prob in danger_heur:
                    #print(f"위치: [{pos[0]}, {pos[1]}], 확률: {prob}, 거리: {path_costs[pos]}")
                    if path_costs[pos] != 1:
                        continue
                    elif (path_costs[pos] == 1 and prob < 100 
                        and self.visited.count([pos[0], pos[1]]) < 1):
                        if [before_x+1, before_y] == [pos[0], pos[1]]:
                            self.agent['xy'] = [pos[0], pos[1]]
                            self.update_visited(pos[0], pos[1])
                            self.agent['dir'] = "South"
                            return ["BestWay", dir, "South"]
                        elif [before_x, before_y+1] == [pos[0], pos[1]]:
                            self.agent['xy'] = [pos[0], pos[1]]
                            self.update_visited(pos[0], pos[1])
                            self.agent['dir'] = "East"
                            return ["BestWay", dir, "East"]
                        elif [before_x-1, before_y] == [pos[0], pos[1]]:
                            self.agent['xy'] = [pos[0], pos[1]]
                            self.update_visited(pos[0], pos[1])
                            self.agent['dir'] = "North"
                            return ["BestWay", dir, "North"]
                        elif [before_x, before_y-1] == [pos[0], pos[1]]:
                            self.agent['xy'] = [pos[0], pos[1]]
                            self.update_visited(pos[0], pos[1])
                            self.agent['dir'] = "West"
                            return ["BestWay",dir, "West"]
                        #print(f"count: [{pos[0]}, {pos[1]}] = {self.visited.count([pos[0], pos[1]])}")
                        
                    if (path_costs[pos] == 1 and prob < 100):
                        
                        temp = self.visited.count([pos[0], pos[1]])
                        if min_visit[1] > temp:
                            min_visit[1] = temp
                            min_visit[0] = [pos[0], pos[1]]
                        print(f"min: {min_visit}")
                if min_visit[0] != None:
                    print(min_visit[0])
                    pos = min_visit[0]
                    if [before_x+1, before_y] == [pos[0], pos[1]]:
                        self.agent['xy'] = [pos[0], pos[1]]
                        self.update_visited(pos[0], pos[1])
                        self.agent['dir'] = "South"
                        return ["BestWay", dir, "South"]
                    elif [before_x, before_y+1] == [pos[0], pos[1]]:
                        self.agent['xy'] = [pos[0], pos[1]]
                        self.update_visited(pos[0], pos[1])
                        self.agent['dir'] = "East"
                        return ["BestWay", dir, "East"]
                    elif [before_x-1, before_y] == [pos[0], pos[1]]:
                        self.agent['xy'] = [pos[0], pos[1]]
                        self.update_visited(pos[0], pos[1])
                        self.agent['dir'] = "North"
                        return ["BestWay", dir, "North"]
                    elif [before_x, before_y-1] == [pos[0], pos[1]]:
                        self.agent['xy'] = [pos[0], pos[1]]
                        self.update_visited(pos[0], pos[1])
                        self.agent['dir'] = "West"
                        return ["BestWay",dir, "West"]
            # agent의 기본 행동
            self.agent['xy'] = [after_x, after_y]
            self.update_visited(after_x, after_y)
            return ["GoForward", dir, percept.sense_breeze(self), percept.sense_stench(self)]
    
        
# def main(self):
    
#     result = reasoning(self)
#     while result[0] != "Grab":
#         print("visited")
#         print(self.visited)
#         print("danger")
#         for row in self.danger_prob:
#             print(row)
#         result = reasoning(self)
#         print(result)

# main(self.init_world())

    
