import pygame
import random
from time import sleep
from SetWorld import init_world
from action import *
random.seed(12) # 1005, 1020, 1031

def load_img():
    #아이템 이미지 불러오기
    wumpus = pygame.image.load('./wumpus-world/Wumpus World_images/wumpus.png')
    wumpus = pygame.transform.scale(wumpus,(100,100))
    pitch = pygame.image.load('./wumpus-world/Wumpus World_images/pitch.png')
    pitch = pygame.transform.scale(pitch,(100,100))
    gold = pygame.image.load('./wumpus-world/Wumpus World_images/gold.png')
    gold = pygame.transform.scale(gold,(100,100))
    #캐릭터 불러오기
    character = pygame.image.load('./wumpus-world/Wumpus World_images/Izreal.png')
    character = pygame.transform.scale(character,(100,100))
    #배경 이미지 불러오기
    background = pygame.image.load('./wumpus-world/Wumpus World_images/grid.png')
    background = pygame.transform.scale(background,(500,500))
    
    arrow = pygame.image.load('./wumpus-world/Wumpus World_images/arrow.png')
    arrow = pygame.transform.scale(arrow,(90,90))

    return [wumpus, pitch, gold, character, background,arrow]

def draw_items(world):
    wumpus = load_img()[0]
    pitch = load_img()[1] 
    gold = load_img()[2]
    grid = load_img()[4]
    screen.blit(grid, (100, 50))
    #아이템 위치지정
    for x,row in enumerate(world.world):
        for y,i in enumerate(row):
            if i == 'W':
                screen.blit(wumpus,(115 + (y-1)*125,70 + (x-1)*125))
            elif i == 'P':
                screen.blit(pitch,(115 + (y-1)*125,70 + (x-1)*125))
            elif i == 'G':
                screen.blit(gold,(115 + (y-1)*125,70 + (x-1)*125))

                 
def rotate(character_info, dir, state, world):
    character = character_info[0]
    character_x_pos = character_info[1]
    character_y_pos = character_info[2]
    east_character = character_info[4]
    west_character = character_info[5]

    while dir != state:
        if dir == "East":
            dir = "North"
            character = pygame.transform.rotate(east_character, 90)
        elif dir == "West":
            dir = "South"
            character = pygame.transform.rotate(west_character, 90)
        elif dir == "North":
            dir = "West"
            character = west_character
        elif dir == "South":
            dir = "East"
            character = east_character
        world.agent['dir'] = dir
        
        screen.fill((255, 255, 255))
        screen.blit(character, (character_x_pos, character_y_pos)) #배경에 캐릭터 그려주기
        draw_items(world)
        pygame.display.update()
        sleep(0.5)
    return character

def move_pos(character_info, dir):
    character = character_info[0]
    character_x_pos = character_info[1]
    character_y_pos = character_info[2]
    charcter_move = character_info[3]

    if dir == "East":
        character_x_pos += charcter_move
    elif dir == "West":
        character_x_pos -= charcter_move
    elif dir == "North":
        character_y_pos -= charcter_move
    elif dir == "South":
        character_y_pos += charcter_move
    
    return [character_x_pos, character_y_pos]


def gui():
    world = init_world()
    
    pygame.init() #초기화 
    color = (255, 255, 255)
    #화면 크기 설정
    screen_width = 710 #가로 크기
    screen_height = 610 #세로 크기
    global screen
    screen = pygame.display.set_mode((screen_width, screen_height))
    screen.fill(color)

    #화면 타이틀 설정
    pygame.display.set_caption("Wumpus World")
    
    #FPS 설정
    clock = pygame.time.Clock()
    
    
    # 이미지 불러오기
    character = load_img()[3]
    character_size = character.get_rect().size #캐릭터 이미지 사이즈 구하기
    character_width = character_size[0] #캐릭터 가로 크기
    character_height = character_size[1] #캐릭터 세로 크기
    

    #캐릭터의 기준 좌표를 캐릭터의 왼쪽 상단으로 둔다.
    character_x_pos = 120 #화면 가로 절반의 중간에 위치. 좌우로 움직이는 변수
    character_y_pos = 530 - character_height #이미지가 화면 세로의 가장 아래 위치  
    screen.blit(character, (character_x_pos, character_y_pos)) #배경에 캐릭터 그려주기
                
    # 캐릭터 모양 유지 용 변수
    east_character = character
    west_character = pygame.transform.flip(character, True, False)

    #캐릭터 이동 거리
    charcter_move = 125
    

    #이벤트 루프
    running = True #게임 진행 여부에 대한 변수 True : 게임 진행 중
    world.update_visited(world.agent['xy'][0], world.agent['xy'][1])

    # 배경 불러오기
    background = load_img()[4]
    screen.blit(background,(100,50)) #배경에 이미지 그려주고 위치 지정
    draw_items(world)

    while running:
        
        for event in pygame.event.get(): #이벤트의 발생 여부에 따른 반복문
            if event.type == pygame.QUIT: #창을 닫는 이벤트 발생했는가?
                running = False
            else:
                character_info = [character, character_x_pos, character_y_pos, charcter_move, east_character, west_character]

                print("visited")
                print(world.visited)
                
                print("danger")
                for row in world.danger_prob:
                    print(row)

                pygame.display.update()
                sleep(0.5)
                print("현재 위치는: ")
                print(world.agent['xy'])
                runGame = reasoning(world)
                print(runGame[0])
                if runGame[0] == "Die":
                    character_x_pos = 120 
                    character_y_pos = 530 - character_height
                    character = east_character
                elif runGame[0] == "Bump" or runGame[0] == "Danger":
                    print(runGame[1])
                    if runGame[1] == "turnLeft":
                        character = pygame.transform.rotate(character, 90)
                    elif runGame[1] == "turnRight":
                        character = pygame.transform.rotate(character, -90)
                    if world.agent['dir'] == "West":
                        character = west_character
                    elif world.agent['dir'] == "East":
                        character = east_character
                elif runGame[0] == "GoForward":
                    dir = runGame[1]
                    result = move_pos(character_info, world.agent['dir'])
                    character_x_pos = result[0]
                    character_y_pos = result[1]
                elif runGame[0] == "Shoot":
                    arrow = load_img()[5]        
                    screen.blit(arrow,(10,10))
                    pygame.display.update()
                    sleep(0.5)
                    print("남은 화살: ")
                    print(runGame[1])
                elif runGame[0] == "BestWay":
                    dir = runGame[1]
                    character = rotate(character_info, dir, runGame[2], world)
                    result = move_pos(character_info, world.agent['dir'])
                    character_x_pos = result[0]
                    character_y_pos = result[1]
                elif runGame[0] == "Grab":
                    # 시작 지점으로 다시 돌아가는 gui
                    path = runGame[1]
                    #print(path)
                    path.pop()
                    while path:
                        route = path.pop()
                        print("가보자고!")
                        print(route)
                        if route[0] == world.agent['xy'][0]:
                            if route[1] == world.agent['xy'][1]+1:
                                character = rotate(character_info, world.agent['dir'], "East",world)
                                
                            elif route[1] == world.agent['xy'][1]-1:
                                character = rotate(character_info,world.agent['dir'], "West", world)
                                
                        elif route[1] == world.agent['xy'][1]:
                            if route[0] == world.agent['xy'][0]+1:
                                character = rotate(character_info, world.agent['dir'], "South", world)
                            
                            elif route[0] == world.agent['xy'][0]-1:
                                character = rotate(character_info, world.agent['dir'], "North", world)
                        character_info[1], character_info[2] = move_pos(character_info, world.agent['dir'])
                        if world.agent['dir'] == "East":
                            character = east_character
                        elif world.agent['dir'] == "West":
                            character = west_character
                        print(route)
                        world.agent['xy'] = route
                        screen.fill(color)
                        screen.blit(character, (character_info[1], character_info[2])) #배경에 캐릭터 그려주기
                        draw_items(world)
                        pygame.display.update()
                        sleep(0.5)

                        # Climb
                        if route == (4, 1):
                            print("FINISH!!!")
                            character = east_character
                            screen.fill((255, 255, 255))
                            screen.blit(character, (character_info[1], character_info[2])) #배경에 캐릭터 그려주기
                            draw_items(world)
                            pygame.display.update()
                            sleep(10)
                            running = False

                            
                      
                print("\n")    

                #왼쪽, 오른쪽 경계 정하기
                if character_x_pos < 120:
                    character_x_pos = 120
            
                elif character_x_pos > 120 + charcter_move * 3 :
                    character_x_pos = 120 + charcter_move * 3
            
                #위, 아래쪽 경계 정하기
                if character_y_pos < 530 - character_height - charcter_move * 3:
                    character_y_pos = 530 - character_height - charcter_move * 3
            
                elif character_y_pos > 530 - character_height :
                    character_y_pos = 530 - character_height 

                # 이미지 리로드
                screen.fill(color)

                screen.blit(background,(100,50)) #배경에 이미지 그려주고 위치 지정
                draw_items(world)
                
                                        
                screen.blit(character, (character_x_pos, character_y_pos)) #배경에 캐릭터 그려주기
                pygame.display.update()
                
                
            
                
        
    #pygame 종료
    pygame.quit()
    
def main():
    gui()
    
    
if __name__ == "__main__":
    main()
        