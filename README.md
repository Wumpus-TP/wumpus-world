# Agent’s moving decision algorithm

1. Default: goForward()
2. 방문한 위치를 visited에 append
3. 위험하지 않으며 방문하지 않은 위치를 방문하는 게 우선

<aside>
💡 danger_prob[x][y] == 0 and in visited

</aside>

1. 바로 앞 격자에 방문한 적 없고, wumpus가 있을 위험이 있으면 shoot

<aside>
💡 danger_prob[x][y][0] > 2, shoot

</aside>

1. 벽에 부딪히면(Bump), turnLeft or turnRight
2. 인접 격자에 모두 방문한 기록이 있다면 덜 위험 격자를 방문

<aside>
💡 If all neighbor node in visited,

A* algorithm 이용: cost가 1이고 heuristic(danger_prob[0]+[1] = sorted 오름차순)

</aside>

1. 최근 2번 이상 방문한 적 있는 격자는 방문하지 않음

<aside>
💡 예를 들어, (1, 1) → (1, 2) → (1, 1) → (1, 2) 인 경우는 (1, 1)은 제외하고 움직인다.

</aside>

1. 현재 노드에 pitch or wumpus가 존재한다면 ,die + 시작 노드로 돌아감
2. 현재 노드에 glitter이 느껴지면, 금 획득(grab)
3. 금을 획득 후, 제자리에 돌아갈 때는 격자 중 방문한 적 있는 격자들 중 시작 위치와 도착 위치를 기준으로 가장 움직임이 적은 격자들을 따라 움직임

<aside>
💡 If grab the gold,
A* algorithm 이용: 방문한 적 있는 격자에 한해서 heuristic(현재 격자에서 시작 지점까지 거리) 계산

</aside>

# The probaility of existing Wumpus, Pitch

var `danger_prob` 

Init : 모든 원소가 [1,1]로 초기화 된 6×6 리스트

원소의 0번째 인덱스 : wumpus의 위험도

원소의 1번째 인덱스 : pitch의 위험도

`update_danger_prob` 함수를 통해 `danger_prob`를 업데이트 하고, 그 안에서wumpus와 pitch의 위치를 논리적으로 추론하는 KB를 구현하였다.

- `update_danger_prob`  알고리즘
1. 현재 위치에 대해서
    1. wumpus가 존재할 경우 현재 위치에 해당하는 `danger_prob`를 [100,0]으로 업데이트
    2. pitch가 존재할 경우 현재 위치에 해당하는 `danger_prob`를 [0,100]으로 업데이트
    3. 둘 다 없을 경우 현재 위치는 안전하므로 [0,0]으로 변경
    4. stench나 breeze가 느껴질 경우 `caution_grid` 딕셔너리에서 해당하는 key(stench, breeze)에 현재 위치 저장
2. 주변 그리드에 대해서
    1. 현재위치에서 stench가 느껴질경우, 주변 그리드 중 이미 wumpus가 없다고 판단(`danger_prob[x][y][0]`== 0)했거나 wumpus가 있다고 판단(`danger_prob[x][y][0]` == 100)한 칸을 제외하고, 나머지 주변 그리드에 대해서 `danger_prob[x][y][0]` += 1을 진행하여 위험도를 올림
    2. 현재위치에서 breeze가 느껴질경우, 주변 그리드 중 이미 pitch가 없다고 판단(`danger_prob[x][y][1]` == 0)했거나 pitch가 있다고 판단(`danger_prob[x][y][1]` == 100)한 칸을 제외하고, 나머지 주변 그리드에 대해서 `danger_prob[x][y][1]` += 1을 진행하여 위험도를 올림
3.  stench나 breeze가 있는 그리드의 주변 그리드에 대해 KB를 이용해 추론
    1. KB는 stench혹은 breeze가 있는 그리드의 주변 그리드에 wumpus 혹은 pitch를 추론하는 과정
    2. 주변 그리드 중 오직 하나의 그리드에서만 위험도가 0이 아니라면, 그 그리드에 wumpus나 pitch가 존재한다고 추론 가능하므로 해당하는 위험에 맞춰 `danger_prob`를 [100,0] 혹은 [0,100]으로 업데이트
    3. wumpus와 pitch는 동시에 존재할 수 없그므로 어떤 그리드에 wumpus가 존재하면 해당 그리드에서 pitch의 `danger_prob`를 0으로 바꾸고, pitch가 존재한다면 해당 그리드에서 wumpus의 `danger_prob`를 0으로 바꾼다.

[wumpus world 작업일지]
| 이름 |	날짜 |
| --- | --- |
| 아이디어 회의	| 2023년 5월 4일 → 2023년 5월 15일 |
| 초기환경 구축 및 위험확률 세팅 |	2023년 5월 11일 → 2023년 5월 21일 |
| action 및 reasoning 함수 구현	| 2023년 5월 18일 → 2023년 5월 28일 |
| percept 함수 구현	| 2023년 5월 18일 → 2023년 5월 22일 |
| gui 구현 |	2023년 5월 27일 → 2023년 5월 30일 |
| 피드백 및 수정 |	2023년 5월 30일 → 2023년 6월 4일 |

