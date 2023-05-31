import pygame

# 격자 크기 및 사각형 크기 설정
GRID_SIZE = 700
GRID_COUNT = 4
RECT_WIDTH = 125
RECT_HEIGHT = 10

# 격자 사이의 간격 계산
GAP = 500
# Pygame 초기화
pygame.init()
window = pygame.display.set_mode((GRID_SIZE, GRID_SIZE))
pygame.display.set_caption("Grid Collision")

# 캐릭터 초기 위치
character_x = RECT_WIDTH // 2
character_y = RECT_HEIGHT // 2

while True:
    for event in pygame.event.get():
        if event.type == pygame.QUIT:
            pygame.quit()
            exit()

    # 캐릭터 이동
    keys = pygame.key.get_pressed()
    if keys[pygame.K_LEFT]:
        character_x -= 1
        if character_x < RECT_WIDTH // 2:
            character_x = RECT_WIDTH // 2
    elif keys[pygame.K_RIGHT]:
        character_x += 1
        if character_x > 700 - (RECT_WIDTH // 2 + 1):
            character_x = 700 - (RECT_WIDTH // 2 + 1)
    elif keys[pygame.K_UP]:
        character_y -= 1
        if character_y < RECT_HEIGHT // 2:
            character_y = RECT_HEIGHT // 2
    elif keys[pygame.K_DOWN]:
        character_y += 1
        if character_y > 700 - (RECT_HEIGHT // 2 + 1):
            character_y = 700 - (RECT_HEIGHT // 2 + 1)

    # 화면 초기화
    window.fill((255, 255, 255))

    for x in range(0, 6):
        for y in range(0, 6):
            #그리드 생성
            if y == 0 and not x > 3:
                pygame.draw.rect(window, (0,0,0), (600, 50+127*x, 10, 127))
            elif y == 5 and not x > 3:
                pygame.draw.rect(window, (0,0,0), (100, 50+127*x, 10, 127))
            if (x == 0 or x == 5) and not y > 3:
                pygame.draw.rect(window, (0, 0, 0), (100+127*y, 50+100*x, 127, 10))
            
    # # 격자와 사각형 그리기
    # for i in range(GRID_COUNT):
    #     pygame.draw.rect(window, (0,0,0), (0, 10+125*i, 10, 125))
    #     pygame.draw.rect(window, (0,0,0), (500, 10+127.5*i, 10, 128))
    #     if (0 <= character_x <= 10 and 10+125*i <= character_y <= 10+125*i+10):
    #         pygame.draw.rect(window, (255, 0, 0), (0, 10+125*i, 10, 125))
    #     elif (500 <= character_x <= 510 and 10+127.5*i <= character_y <= 10+127.5*i+10):
    #         pygame.draw.rect(window, (255,0,0), (500, 10+127.5*i, 10, 128))
    #     for j in range(2):
    #         rect_x = RECT_WIDTH * i
    #         rect_y = 10 + GAP * j
    #         pygame.draw.rect(window, (0, 0, 0), (rect_x, rect_y, RECT_WIDTH, RECT_HEIGHT))

    #         # 캐릭터와 충돌한 격자를 빨간색 사각형으로 표시
    #         if (rect_x <= character_x <= rect_x + RECT_WIDTH and
    #                 rect_y <= character_y <= rect_y + RECT_HEIGHT):
    #             pygame.draw.rect(window, (255, 0, 0), (rect_x, rect_y, RECT_WIDTH, RECT_HEIGHT))
            

    # 캐릭터 그리기
    pygame.draw.circle(window, (0, 0, 255), (character_x, character_y), 5)

    pygame.display.update()
