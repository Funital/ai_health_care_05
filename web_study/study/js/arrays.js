// 배열
let numbers = [10,20,30,"40"];

console.log(typeof numbers); // object
for(let i=0; i < numbers.length; i++) {
    console.log(numbers[i]);
}

for (const [i,n] of numbers.entries()) {
    console.log(i, n);
}