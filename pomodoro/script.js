const workMinutesInput = document.getElementById('workMinutes');
const shortBreakMinutesInput = document.getElementById('shortBreakMinutes');
const timerDisplay = document.getElementById('timerDisplay');
const statusText = document.getElementById('statusText');
const completedCountText = document.getElementById('completedCount');
const startPauseBtn = document.getElementById('startPauseBtn');
const resetBtn = document.getElementById('resetBtn');
const ringProgress = document.querySelector('.ring-progress');

const RING_RADIUS = 140;
const RING_CIRCUMFERENCE = 2 * Math.PI * RING_RADIUS;
const WORK_MODE = 'work';
const BREAK_MODE = 'break';
const LONG_BREAK_MINUTES = 15;
const STORAGE_KEY = 'pomodoro-today-count';

let timer = null;
let mode = WORK_MODE;
let remainingSeconds = 25 * 60;
let totalSeconds = 25 * 60;
let isRunning = false;
let completedCount = 0;
let todayKey = '';

function formatTime(seconds) {
  const m = Math.floor(seconds / 60).toString().padStart(2, '0');
  const s = Math.floor(seconds % 60).toString().padStart(2, '0');
  return `${m}:${s}`;
}

function updateRing() {
  const progress = totalSeconds > 0 ? remainingSeconds / totalSeconds : 0;
  const offset = RING_CIRCUMFERENCE * (1 - progress);
  ringProgress.style.strokeDasharray = `${RING_CIRCUMFERENCE} ${RING_CIRCUMFERENCE}`;
  ringProgress.style.strokeDashoffset = offset;
}

function updateTheme() {
  document.body.classList.toggle('work-mode', mode === WORK_MODE);
  document.body.classList.toggle('break-mode', mode === BREAK_MODE);
  statusText.textContent = mode === WORK_MODE ? '專注中' : '休息中';
}

function updateDisplay() {
  timerDisplay.textContent = formatTime(remainingSeconds);
  completedCountText.textContent = completedCount;
  updateTheme();
  updateRing();
}

function loadCompletedCount() {
  const stored = localStorage.getItem(STORAGE_KEY);
  const today = new Date().toISOString().slice(0, 10);
  todayKey = today;

  if (!stored) {
    completedCount = 0;
    return;
  }

  try {
    const data = JSON.parse(stored);
    if (data.date === today) {
      completedCount = data.count || 0;
    } else {
      completedCount = 0;
    }
  } catch {
    completedCount = 0;
  }
}

function saveCompletedCount() {
  const payload = { date: todayKey, count: completedCount };
  localStorage.setItem(STORAGE_KEY, JSON.stringify(payload));
}

function requestNotificationPermission() {
  if (!('Notification' in window)) return;
  if (Notification.permission === 'default') {
    Notification.requestPermission();
  }
}

function showSessionNotification() {
  if (!('Notification' in window) || Notification.permission !== 'granted') {
    return;
  }

  new Notification('休息一下吧！', {
    body: '時間到，可以休息或走動一下。',
    icon: 'https://raw.githubusercontent.com/github/explore/main/topics/pomodoro/pomodoro.png'
  });
}

function playAlertSound() {
  try {
    const AudioContext = window.AudioContext || window.webkitAudioContext;
    const ctx = new AudioContext();
    const oscillator = ctx.createOscillator();
    const gain = ctx.createGain();
    oscillator.type = 'sine';
    oscillator.frequency.value = 880;
    gain.gain.value = 0.15;
    oscillator.connect(gain);
    gain.connect(ctx.destination);
    oscillator.start();
    oscillator.stop(ctx.currentTime + 0.35);
    oscillator.onended = () => ctx.close();
  } catch (error) {
    console.warn('音訊播放失敗', error);
  }
}

function calculateSessionDuration() {
  const work = Number(workMinutesInput.value) || 1;
  const rest = Number(shortBreakMinutesInput.value) || 1;

  if (mode === WORK_MODE) {
    totalSeconds = work * 60;
  } else {
    const nextBreak = completedCount > 0 && completedCount % 4 === 0 ? LONG_BREAK_MINUTES : rest;
    totalSeconds = nextBreak * 60;
  }
  remainingSeconds = totalSeconds;
}

function handleSessionEnd() {
  playAlertSound();
  showSessionNotification();

  if (mode === WORK_MODE) {
    completedCount += 1;
    saveCompletedCount();
    mode = BREAK_MODE;
  } else {
    mode = WORK_MODE;
  }

  const nextDuration = mode === WORK_MODE
    ? (Number(workMinutesInput.value) || 1)
    : (completedCount > 0 && completedCount % 4 === 0 ? LONG_BREAK_MINUTES : (Number(shortBreakMinutesInput.value) || 1));

  totalSeconds = nextDuration * 60;
  remainingSeconds = totalSeconds;
  isRunning = false;
  clearInterval(timer);
  timer = null;
  startPauseBtn.textContent = '開始';
  updateDisplay();
}

function tick() {
  if (remainingSeconds <= 0) {
    handleSessionEnd();
    return;
  }

  remainingSeconds -= 1;
  updateDisplay();
}

function startTimer() {
  if (isRunning) return;
  if (!timer) {
    if (!totalSeconds || remainingSeconds === 0) {
      calculateSessionDuration();
    }
  }
  timer = setInterval(tick, 1000);
  isRunning = true;
  startPauseBtn.textContent = '暫停';
}

function pauseTimer() {
  if (!isRunning) return;
  clearInterval(timer);
  timer = null;
  isRunning = false;
  startPauseBtn.textContent = '開始';
}

function resetTimer() {
  pauseTimer();
  mode = WORK_MODE;
  const workMinutes = Number(workMinutesInput.value) || 25;
  totalSeconds = workMinutes * 60;
  remainingSeconds = totalSeconds;
  startPauseBtn.textContent = '開始';
  updateDisplay();
}

startPauseBtn.addEventListener('click', () => {
  requestNotificationPermission();
  if (isRunning) {
    pauseTimer();
  } else {
    if (remainingSeconds === 0) {
      calculateSessionDuration();
    }
    startTimer();
  }
});

resetBtn.addEventListener('click', () => {
  resetTimer();
});

[workMinutesInput, shortBreakMinutesInput].forEach((input) => {
  input.addEventListener('change', () => {
    const minValue = Number(input.min);
    if (Number(input.value) < minValue) {
      input.value = minValue;
    }
    if (!isRunning) {
      resetTimer();
    }
  });
});

function init() {
  ringProgress.style.strokeDasharray = `${RING_CIRCUMFERENCE} ${RING_CIRCUMFERENCE}`;
  loadCompletedCount();
  resetTimer();
  updateDisplay();
}

init();
