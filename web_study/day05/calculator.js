// 계산기 상태
let isOn = false;
let currentExpression = '';
let isCalculationComplete = false;

// 페이지 로드 시 초기 상태 (OFF)
document.addEventListener('DOMContentLoaded', function () {
    setDisplay('');
});

// --- 사칙연산 함수 ---
function add(a, b) { return a + b; }
function subtract(a, b) { return a - b; }
function multiply(a, b) { return a * b; }
function divide(a, b) { return a / b; }

// --- 디스플레이 헬퍼 ---
function setDisplay(value) {
    document.getElementById('display').value = value;
}

// --- ON/OFF 토글 ---
function togglePower() {
    isOn = !isOn;
    const btn = document.querySelector('.on-off');
    if (isOn) {
        btn.classList.add('on');
        currentExpression = '';
        isCalculationComplete = false;
        setDisplay('0');
    } else {
        btn.classList.remove('on');
        currentExpression = '';
        isCalculationComplete = false;
        setDisplay('');
    }
}

// --- 초기화 ---
function clearDisplay() {
    if (!isOn) return;
    currentExpression = '';
    isCalculationComplete = false;
    setDisplay('0');
}

// --- 숫자/소수점 입력 ---
function appendNumber(num) {
    if (!isOn) return;

    // 계산 직후 새 숫자 입력 시 초기화
    if (isCalculationComplete) {
        currentExpression = '';
        isCalculationComplete = false;
    }

    // 같은 숫자 파트에 소수점 중복 방지
    if (num === '.') {
        const lastNumber = currentExpression.split(/[+\-*/]/).pop();
        if (lastNumber.includes('.')) return;
        if (lastNumber === '') currentExpression += '0'; // 연산자 직후 '.' 입력 시 '0.' 처리
    }

    currentExpression += num;
    setDisplay(currentExpression);
}

// --- 연산자 입력 ---
function appendOperator(op) {
    if (!isOn) return;
    if (currentExpression === '') return;

    isCalculationComplete = false;

    // 마지막 문자가 연산자면 교체
    const lastChar = currentExpression.slice(-1);
    if (['+', '-', '*', '/'].includes(lastChar)) {
        currentExpression = currentExpression.slice(0, -1) + op;
    } else {
        currentExpression += op;
    }

    setDisplay(currentExpression);
}

// --- 계산 처리 (사칙연산 우선순위 적용) ---
function calculate(formula) {
    const tokens = formula.replace(/\s+/g, '').match(/\d+(\.\d+)?|[+\-*/]/g);
    if (!tokens || tokens.length < 3 || tokens.length % 2 === 0) {
        return '잘못된 계산식';
    }

    // 1단계: 곱셈, 나눗셈 먼저 처리
    const intermediate = [];
    let i = 0;
    while (i < tokens.length) {
        const token = tokens[i];
        if (token === '*' || token === '/') {
            const left = Number(intermediate.pop());
            const right = Number(tokens[i + 1]);
            if (isNaN(left) || isNaN(right)) return '잘못된 숫자';
            if (token === '/' && right === 0) return '0으로 나눌 수 없습니다';
            intermediate.push(token === '*' ? multiply(left, right) : divide(left, right));
            i += 2;
        } else {
            intermediate.push(token);
            i++;
        }
    }

    // 2단계: 덧셈, 뺄셈 처리
    let result = Number(intermediate[0]);
    if (isNaN(result)) return '잘못된 숫자';

    for (let j = 1; j < intermediate.length; j += 2) {
        const op = intermediate[j];
        const next = Number(intermediate[j + 1]);
        if (isNaN(next)) return '잘못된 숫자';
        if (op === '+') result = add(result, next);
        else if (op === '-') result = subtract(result, next);
    }

    return result;
}

// --- Enter: 계산 실행 ---
function performCalculate() {
    if (!isOn) return;
    if (currentExpression === '') return;

    const result = calculate(currentExpression);

    if (typeof result === 'string') {
        // 에러 메시지 표시 후 초기화
        setDisplay(result);
        currentExpression = '';
    } else {
        setDisplay(result);
        currentExpression = String(result);
        isCalculationComplete = true;
    }
}
