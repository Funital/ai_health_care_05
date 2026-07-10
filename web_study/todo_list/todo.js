// DOM 요소
const addBtn = document.querySelector("#add-btn");
const todoInput = document.querySelector("#todo-input");
const todoList = document.querySelector("#todo-list");

// 상태
let todos = JSON.parse(localStorage.getItem("todos")) || [];

// 스토리지
function saveTodos() {
    localStorage.setItem("todos", JSON.stringify(todos));
}

// 삭제 버튼 생성
function createDeleteButton(index) {
    const btn = document.createElement("button");
    btn.className = "btn btn-danger btn-sm";
    btn.textContent = "삭제";
    btn.addEventListener("click", () => deleteTodo(index));
    return btn;
}

// 할 일 항목(li) 생성
function createTodoItem(text, index) {
    const li = document.createElement("li");
    li.className = "list-group-item d-flex justify-content-between align-items-center";
    li.textContent = text;
    li.appendChild(createDeleteButton(index));
    return li;
}

// 목록 렌더링
function renderTodos() {
    todoList.innerHTML = "";
    todos.forEach((text, index) => {
        todoList.appendChild(createTodoItem(text, index));
    });
}

// 할 일 추가
function addTodo() {
    const text = todoInput.value.trim();
    if (!text) {
        alert("할 일을 입력해주세요.");
        return;
    }
    todos.push(text);
    todoInput.value = "";
    saveTodos();
    renderTodos();
}

// 할 일 삭제
function deleteTodo(index) {
    todos = todos.filter((_, i) => i !== index);
    saveTodos();
    renderTodos();
}

// 이벤트 리스너
addBtn.addEventListener("click", addTodo);
todoInput.addEventListener("keydown", (e) => {
    if (e.key === "Enter" && !e.isComposing) addTodo();
});

// 초기화
renderTodos();
