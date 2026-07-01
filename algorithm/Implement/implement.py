"""
    [상하좌우]
    첫째 줄에 공간의 크기를 나타내는 N이 주어짐. (1 ≤ N ≤ 100)
    둘째 줄에 여행가 A가 이동할 계획서 내용이 주어진다. (1 ≤ 이동 횟수 ≤ 100)
    여행가 A는 항상 (1, 1) 좌표에서 시작하며, 계획서에 따라 이동한 뒤 최종적으로 도착할 지점의 좌표를 출력한다

    예시) 
    5
    R R R U D D   ->   3 4(결과, 최종 좌표)
"""
# space_size = int(input('공간의 크기 N을 입력하세요: '))
# plans = list(map(str, input('이동 계획서를 입력하세요: ').split()))

# # 초기 위치(x, y)
# x, y = 1, 1

# # 이동 방향 -> 좌표니까.
# dx = [-1, 1, 0, 0]  # U, D, L, R
# dy = [0, 0, -1, 1]


# # 계획서에 따라 이동
# for plan in plans:
#     if plan == 'U':
#         nx, ny = x + dx[0], y + dy[0]
#     elif plan == 'D':
#         nx, ny = x + dx[1], y + dy[1]
#     elif plan == 'L':
#         nx, ny = x + dx[2], y + dy[2]
#     elif plan == 'R':
#         nx, ny = x + dx[3], y + dy[3]

#     # 공간을 벗어나지 않도록 조건 추가
#     if 1 <= nx <= space_size and 1 <= ny <= space_size:
#         x, y = nx, ny

# print(x, y)

"""
    [시각]
    첫째 줄에 정수 N이 주어진다. (0 ≤ N ≤ 23)
    00시 00분 00초부터 N시 59분 59초까지의 모든 시각 중에서 3이 하나라도 포함되는 모든 경우의 수를 구하는 프로그램을 작성하시오.

    예시) 
    5  ->   11475
"""
# num = int(input('정수 N을 입력하세요: '))
# count = 0

# for hour in range(num + 1):
#     for minute in range(60):
#         for second in range(60):
#             if '3' in str(hour) + str(minute) + str(second):
#                 count += 1

# print(count)

"""
    [왕실의 나이트]
    첫째 줄에 8x8 좌표 평면상에서 나이트의 위치가 주어진다. -> (a~h)(1~8)
    나이트가 이동할 수 있는 경우의 수 출력하기.(나이트는 이동 시 L자 형태로 이동)

    예시) 
    a1  ->   2
"""
# n = input('나이트의 위치를 입력하세요: ')

# row = int(n[1])
# column = int(ord(n[0])) - int(ord('a')) + 1

# steps = [(-2, -1), (-2, 1), (-1, -2), (-1, 2), (1, -2), (1, 2), (2, -1), (2, 1)]

# result = 0
# for step in steps:
#     next_row = row + step[0]
#     next_column = column + step[1]

#     if 1 <= next_row <= 8 and 1 <= next_column <= 8:
#         result += 1

# print(result)

"""
    [게임 개발]
    첫째 줄에 맵의 세로 크기 N과 가로 크기 M을 공백으로 구분하여 입력한다. (3 ≤ N, M ≤ 50)
    둘째 줄에 게임 캐릭터가 있는 칸의 좌표 (A,B)와 바라보는 방향 d가 공백으로 구분하여 주어진다.
    - 방향 d의 값은 다음과 같다. (0:북쪽, 1:동쪽, 2:남쪽, 3:서쪽)
    셋째 줄부터 맵이 육지인지 바다인지에 대한 정보가 주어진다. (0:육지, 1:바다)
    게임 캐릭터는 상하좌우로 이동할 수 있으며, 바다로 되어 있는 공간에는 갈 수 없다. 게임 캐릭터의 이동 계획에 따라 최종적으로 방문한 칸의 수를 출력하는 프로그램을 작성하시오.

    예시) 
    4 4
    1 1 0
    1 1 1 1
    1 0 0 1
    1 1 0 1
    1 1 1 1   ->   3
"""
n, m = map(int, input().split())

# 방문 위치를 저장하기 위한 맵 초기화
d = [[0] * m for _ in range(n)]

# 현재 캐릭터의 X 좌표, Y 좌표, 방향을 입력받기
x, y, direction = map(int, input().split())
d[x][y] = 1  # 현재 좌표 방문 처리

# 전체 맵 정보를 입력받기
array = []
for i in range(n):
    array.append(list(map(int, input().split())))

# 북, 동, 남, 서 방향 정의
dx = [-1, 0, 1, 0]
dy = [0, 1, 0, -1]

# 왼쪽으로 회전
def turn_left():
    global direction
    direction -= 1
    if direction == -1:
        direction = 3

# 시뮬레이션 시작
count = 1
turn_time = 0
while True:
    # 왼쪽으로 회전
    turn_left()
    nx = x + dx[direction]
    ny = y + dy[direction]

    # 회전한 이후 정면에 가보지 않은 칸이 존재하는 경우 이동
    if d[nx][ny] == 0 and array[nx][ny] == 0:
        d[nx][ny] = 1
        x, y = nx, ny
        count += 1
        turn_time = 0
        continue
    # 회전한 이후 정면에 가보지 않은 칸이 없거나 바다인 경우
    else:
        turn_time += 1

    # 네 방향 모두 갈 수 없는 경우
    if turn_time == 4:
        nx = x - dx[direction]
        ny = y - dy[direction]
        # 뒤로 갈 수 있다면 이동하기
        if array[nx][ny] == 0:
            x, y = nx, ny
        # 뒤가 바다로 막혀있는 경우
        else:
            break
        turn_time = 0

print(count)
