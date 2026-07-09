// FetchAPI
// https://jsonplaceholder.typicode.com/posts

// GET request
// fetch('https://jsonplaceholder.typicode.com/posts')
//   .then(response => response.json()) // 응답 메시지에서 JSON 데이터를 추출
//   .then(data => console.log(data)) // 콘솔에 출력
//   .catch(error => console.error('Error:', error));

// POST request
fetch('https://jsonplaceholder.typicode.com/posts', {
  method: 'POST',
  headers: {
    'Content-Type': 'application/json'
  },
  body: JSON.stringify({
    title: 'foo',
    body: 'bar',
    userId: 1
  })
})
  .then(response => response.json())
  .then(data => console.log(data))
  .catch(error => console.error('Error:', error));
