const timeInput = document.querySelector('#time-input');
const startBtn = document.querySelector('#start-timer');
const stopBtn = document.querySelector('#stop-timer');
const display = document.querySelector('#timer-display');

// 남은 시간
let remainingSeconds = 0;

// 현재 동작 중인 타이머 id
let timerId = null;

function updateDisplay() {
    const minutes = Math.floor(remainingSeconds / 60);
    const seconds = remainingSeconds % 60;
    // const timeToDisplay = `${minutes.toString().padStart(2, '0')}:${seconds.toString().padStart(2, '0')}`;
    const timeToDisplay = String(minutes).padStart(2, '0') + ':' + String(seconds).padStart(2, '0');
    display.textContent = timeToDisplay;
}

// 타이머 시작
startBtn.addEventListener('click', () => {
    const minutes = Number(timeInput.value);
    if (isNaN(minutes) || minutes <= 0) {
        alert('Please enter a valid number of minutes.');
        return;
    }
    remainingSeconds = minutes * 60;
    updateDisplay();

    // 타이머를 1초마다 감소시키는 interval 설정
    timerId = setInterval(
        () => {
            if (remainingSeconds <= 0) {
                clearInterval(timerId);
                alert('Time is up!');
                return;
            }

            remainingSeconds--;
            updateDisplay();
        },
        1000
    );
});

// 타이머 중지
stopBtn.addEventListener('click', () => {
    clearInterval(timerId);
    timerId = null;
});