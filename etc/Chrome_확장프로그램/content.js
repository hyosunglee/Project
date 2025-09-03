
console.log("Starting Browser Cat extension...");

// 확인용으로 간단한 HTML 요소 추가
const testDiv = document.createElement('div');
testDiv.textContent = 'Test element added';
testDiv.style.position = 'fixed';
testDiv.style.top = '10px';
testDiv.style.left = '10px';
testDiv.style.backgroundColor = 'yellow';
testDiv.style.padding = '10px';
document.body.appendChild(testDiv);

console.log("Test element added to the page.");


// 고양이 요소 추가
const cat = document.createElement('div');
cat.id = 'browser-cat';
document.body.appendChild(cat);

// 고양이 움직임
let direction = 1; // 1: 오른쪽, -1: 왼쪽
let position = 20; // 초기 위치

function moveCat() {

  console.log("Browser Cat extension loaded!");
  position += direction * 5; // 고양이 움직임 속도
  cat.style.left = `${position}px`;

  // 화면 경계에서 방향 전환
  if (position > window.innerWidth - 100 || position < 0) {
    direction *= -1;
    cat.style.transform = `scaleX(${direction})`; // 방향 전환
  }
}

setInterval(moveCat, 50); // 매 50ms마다 고양이 이동

// 고양이 클릭 이벤트
cat.addEventListener('click', () => {
  const meowSound = new Audio(chrome.runtime.getURL('sounds/meow.mp3'));
  meowSound.play();
  alert('냐옹! 고양이가 당신을 좋아합니다!'); // 귀여운 반응
});
