const workInput = document.getElementById("workInput");
const breakInput = document.getElementById("breakInput");
const timeDisplay = document.getElementById("timeDisplay");
const startPauseBtn = document.getElementById("startPauseBtn");
const resetBtn = document.getElementById("resetBtn");
const statusLabel = document.getElementById("statusLabel");
const modeLabel = document.getElementById("modeLabel");
const progressBar = document.getElementById("progressBar");
const statusPanel = document.getElementById("statusPanel");
const completedCountEl = document.getElementById("completedCount");

let timer = null;
let remainingSeconds = 25 * 60;
let durationSeconds = 25 * 60;
let isRunning = false;
let sessionType = "work";
let completedCount = 0;
let successfulPomodoros = 0;

const STORAGE_KEY = "pomodoroClockState";
const PROGRESS_CIRCLE_LENGTH = 2 * Math.PI * 100;

function formatTime(seconds) {
  const mins = Math.floor(seconds / 60);
  const secs = seconds % 60;
  return `${String(mins).padStart(2, "0")}:${String(secs).padStart(2, "0")}`;
}

function loadState() {
  try {
    const saved = JSON.parse(localStorage.getItem(STORAGE_KEY) || "null");
    const today = new Date().toISOString().slice(0, 10);
    if (saved?.date === today) {
      completedCount = saved.completedCount || 0;
      successfulPomodoros = saved.successfulPomodoros || 0;
    } else {
      completedCount = 0;
      successfulPomodoros = 0;
      saveState();
    }
  } catch (error) {
    completedCount = 0;
    successfulPomodoros = 0;
  }
}

function saveState() {
  const today = new Date().toISOString().slice(0, 10);
  localStorage.setItem(
    STORAGE_KEY,
    JSON.stringify({ date: today, completedCount, successfulPomodoros })
  );
}

function updateDisplay() {
  timeDisplay.textContent = formatTime(remainingSeconds);
  completedCountEl.textContent = completedCount;
  const ratio = 1 - remainingSeconds / durationSeconds;
  const offset = PROGRESS_CIRCLE_LENGTH * (1 - ratio);
  progressBar.style.strokeDashoffset = Math.max(0, offset);
  progressBar.style.stroke = sessionType === "work" ? "var(--accent-work)" : "var(--accent-break)";
  statusPanel.style.background = sessionType === "work" ? "rgba(255,93,93,0.16)" : "rgba(76,211,125,0.16)";
  statusLabel.textContent = sessionType === "work" ? "專注中" : "休息中";
  modeLabel.textContent = sessionType === "work" ? "工作時間" : successfulPomodoros >= 4 ? "長休息時間" : "休息時間";
  startPauseBtn.textContent = isRunning ? "暫停" : "開始";
}

function setTimerType(type) {
  sessionType = type;
  const workMinutes = Number(workInput.value) || 25;
  const breakMinutes = Number(breakInput.value) || 5;

  if (type === "work") {
    durationSeconds = workMinutes * 60;
  } else {
    durationSeconds = successfulPomodoros >= 4 ? 15 * 60 : breakMinutes * 60;
  }

  remainingSeconds = durationSeconds;
  updateDisplay();
}

function playSound() {
  const audioCtx = new (window.AudioContext || window.webkitAudioContext)();
  const oscillator = audioCtx.createOscillator();
  const gain = audioCtx.createGain();

  oscillator.type = "sine";
  oscillator.frequency.setValueAtTime(880, audioCtx.currentTime);
  gain.gain.setValueAtTime(0.001, audioCtx.currentTime);
  gain.gain.exponentialRampToValueAtTime(0.2, audioCtx.currentTime + 0.05);
  gain.gain.exponentialRampToValueAtTime(0.001, audioCtx.currentTime + 0.8);

  oscillator.connect(gain).connect(audioCtx.destination);
  oscillator.start();
  oscillator.stop(audioCtx.currentTime + 0.9);
}

function notify(message) {
  if (window.Notification && Notification.permission === "granted") {
    new Notification(message);
  } else if (window.Notification && Notification.permission !== "denied") {
    Notification.requestPermission().then((permission) => {
      if (permission === "granted") {
        new Notification(message);
      } else {
        alert(message);
      }
    });
  } else {
    alert(message);
  }
}

function finishSession() {
  playSound();
  if (sessionType === "work") {
    completedCount += 1;
    successfulPomodoros += 1;
    if (successfulPomodoros >= 4) {
      notify("完成 4 個番茄鐘！開始 15 分鐘長休息吧！");
    } else {
      notify("休息一下吧！");
    }
    saveState();
    setTimerType("break");
  } else {
    notify("休息結束，回到工作吧！");
    if (successfulPomodoros >= 4) {
      successfulPomodoros = 0;
    }
    setTimerType("work");
  }
  isRunning = false;
  updateDisplay();
}

function tick() {
  if (remainingSeconds > 0) {
    remainingSeconds -= 1;
    updateDisplay();
  } else {
    clearInterval(timer);
    timer = null;
    finishSession();
  }
}

function startTimer() {
  if (!timer) {
    timer = setInterval(tick, 1000);
  }
  isRunning = true;
  updateDisplay();
}

function pauseTimer() {
  if (timer) {
    clearInterval(timer);
    timer = null;
  }
  isRunning = false;
  updateDisplay();
}

function resetTimer() {
  pauseTimer();
  setTimerType(sessionType);
}

startPauseBtn.addEventListener("click", () => {
  if (isRunning) {
    pauseTimer();
  } else {
    startTimer();
  }
});

resetBtn.addEventListener("click", () => {
  resetTimer();
});

workInput.addEventListener("change", () => {
  if (sessionType === "work") {
    setTimerType("work");
  }
});

breakInput.addEventListener("change", () => {
  if (sessionType === "break") {
    setTimerType("break");
  }
});

document.addEventListener("DOMContentLoaded", () => {
  progressBar.style.strokeDasharray = PROGRESS_CIRCLE_LENGTH;
  progressBar.style.strokeDashoffset = PROGRESS_CIRCLE_LENGTH;
  loadState();
  setTimerType("work");
  updateDisplay();
  if (window.Notification && Notification.permission !== "granted") {
    Notification.requestPermission();
  }
});
