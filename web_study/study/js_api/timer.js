// Timer API

// 1) setTimeout(callback, delay) : 일정 시간 후에 한 번만 실행

// setTimeout(
//     () => {
//         console.log('3초 후에 실행');
//     },
//     3000
// )

// 2) setInterval(callback, delay) : 일정 시간마다 반복 실행
let counter = 0;
const timerId = setInterval(
    () => {
        if (counter === 5) {
            clearInterval(timerId);
            console.log('타이머 종료');
        }
        counter++;
        console.log(`${counter}번째 2초마다 실행`);
    },
    2000
)
console.log(timerId)