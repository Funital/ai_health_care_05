import asyncio
import time

async def async_a():
    print("async_a 시작")
    await asyncio.sleep(2)  # 비동기적으로 2초 대기
    # time.sleep(2)  # 동기적으로 2초 대기 , blocking => a가 끝나야 다음 껄로 넘어감.
    print("async_a 종료")

async def async_b():
    print("async_b 시작")
    await asyncio.sleep(1)  # 비동기적으로 1초 대기
    print("async_b 종료")

async def main():
    c1 = async_a()  # 코루틴 객체
    c2 = async_b()
    await asyncio.gather(c1, c2)  # 동시에 실행

start = time.time()
asyncio.run(main()) # main 코루틴 객체
end = time.time()
print(f"실행 시간 : {end - start:.2f}초")