# 가장 대표적인 문제 - 거스름돈 문제
n = 1260
count = 0

# 큰 단위의 화폐부터 차례대로 확인
coin_types = [500, 100, 50, 10]

# 시간 복잡도 O(K)
for coin in coin_types:
    count += n // coin  # 해당 화폐로 거슬러 줄 수 있는 동전의 개수 세기
    n %= coin  # 거슬러 준 후 남은 금액

print("=== 거스름돈 문제 ===")
print(f"거슬러 줄 동전의 개수: {count}\n")


"""
    [큰 수의 법칙]
    첫째 줄에 N, M, K가 공백으로 구분되어 차례대로 주어진다. (1 ≤ N ≤ 1,000, 1 ≤ M ≤ 1,000, 1 ≤ K ≤ 10,000)
        - N: 배열 크기
        - M: 숫자가 더해지는 횟수
        - K: 연속으로 더해질 수 있는 최대 횟수
    둘째 줄에, N개의 수가 공백으로 구분되어 차례대로 주어진다. (1 ≤ 각 수 ≤ 10,000)
    입력으로 주어지는 K는 항상 M보다 작거나 같다.

    출력은 가장 큰 값 => 가장 큰 수를 K번 더하고, 그 다음으로 큰 수를 한 번 더하는 것을 반복하면 된다.

    예시) 
    5 8 3
    2 4 5 4 6    ->   46(결과, 6+6+6+5+6+6+6+5)
"""
# n, m, k 공백으로 구분해서 입력
n, m, k = map(int, input('N, M, K를 입력하세요: ').split())

# n개 수를 공백으로 구분해 입력받기
data = list(map(int, input().split()))

data.sort()  # 입력받은 수 정렬
first = data[n - 1]  # 가장 큰 수
second = data[n - 2]  # 두 번째로 큰 수

result = 0

# 방법 1
# while True:
#     for i in range(k):  # 가장 큰 수를 K번 더하기
#         if m == 0:  # m이 0이라면 반복문 탈출
#             break
#         result += first
#         m -= 1  # 더할 때마다 1씩 빼기
#     if m == 0:  # m이 0이라면 반복문 탈출
#         break
#     result += second  # 두 번째로 큰 수를 한 번 더하기
#     m -= 1  # 더할 때마다 1씩 빼기

# 방법 2
count = int(m / (k + 1)) * k  # 가장 큰 수가 더해지는 횟수 계산
count += m % (k + 1)  # 나머지 횟수만
result += (count) * first  # 가장 큰 수 더하기
result += (m - count) * second  # 두 번째로 큰 수 더하기

print("=== 큰 수의 법칙 ===")
print(f"결과: {result}\n")

"""
    [숫자 카드 게임]
    첫째 줄에 숫자 카드들이 놓인 행의 개수 N과 열의 개수 M이 공백으로 구분되어 주어진다. (1 ≤ N, M ≤ 100)
    둘째 줄에, N개의 줄에 걸쳐 각 카드에 적힌 숫자가 주어진다. (1 ≤ 각 숫자 ≤ 10000)
    첫째 줄에 게임의 룰에 맞게 선택한 카드에 적힌 숫자를 출력한다.

    예시) 
    3 3
    3 1 2
    4 1 4
    2 2 2   ->   2(결과, 각 행에서 가장 작은 수를 뽑고, 그 중에서 가장 큰 수를 뽑기)
"""

n, m = map(int, input('N, M을 입력하세요: ').split())

result = 0
for i in range(n):
    data = list(map(int, input().split()))

    if len(data) != m:
        print(f"{m}개의 숫자를 입력해야 합니다.")
        exit()

    min_value = min(data)  # 현재 줄에서 가장 작은 수 찾기
    result = max(result, min_value)  # 가장 작은 수들 중에서 가장 큰 수 찾기

print("=== 숫자 카드 게임 ===")
print(f"결과: {result}\n")

"""
    [1이 될 때까지]
    첫째 줄에 N, K가 공백으로 구분되어 차례대로 주어진다. (2 ≤ N ≤ 100,000, 2 ≤ K ≤ 100,000)
    이때, N은 항상 K보다 크거나 같다.
    첫째 줄에 N이 1이 될 때까지 1번 혹은 2번의 과정을 수행해야 하는 최소 횟수를 출력한다.
        1. N에서 1을 뺀다.
        2. N을 K로 나눈다.

    예시) 
    25 5   ->   2
"""

n, k = map(int, input('N, K를 입력하세요: ').split())
result = 0

# 방법 1
# while n >= k:
#     while n % k != 0:  # N이 K로 나누어 떨어지지 않는다면 1씩 빼기
#         n -= 1
#         result += 1
#     n //= k  # K로 나누기
#     result += 1

# 방법 2 - 시간적 효율성
while True:
    target = (n // k) * k  # N이 K로 나누어 떨어지는 수까지 빼기
    result += (n - target)  # 횟수 계산
    n = target  # N을 K로 나누어 떨어지는 수로 변경

    if n < k:  # N이 K보다 작을 때 반복문 탈출
        break

    result += 1  # K로 나누기
    n //= k
result += (n - 1)  # 마지막으로 남은 수에 대해 1씩 빼기

print("=== 1이 될 때까지 ===")
print(f"결과: {result}\n")