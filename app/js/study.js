// Study Mode - Apple Pencil split-view study session
import { openDB, saveAnnotation, loadAnnotation, saveProgress, loadProgress } from './db.js';
import { loadQuestions, qId, getSubjects, getTagsBySubject, filterBySubject, filterByTag } from './store.js';
import { renderQuestionCard, renderMath, setKatexReady } from './render.js';
import {
  initAnnotation, setDrawingMode, setTool, getCurrentTool,
  loadStrokes, clearStrokes, getStrokes, resizeCanvas, flushSave,
} from './annotation.js';

let questions = [];
let currentIndex = 0;
let answered = false;
let userAnswer = null;

// ===========================
// Init
// ===========================

async function init() {
  document.getElementById('loading').style.display = 'flex';

  await openDB();
  const allQuestions = await loadQuestions((pct, msg) => {
    document.getElementById('loading-text').textContent = msg;
  });

  // Parse URL params for filter
  const params = new URLSearchParams(window.location.search);
  const subject = params.get('subject');
  const tag = params.get('tag');
  const startIdx = parseInt(params.get('idx')) || 0;

  if (tag) {
    questions = filterByTag(tag);
  } else if (subject) {
    questions = filterBySubject(subject);
  } else {
    questions = allQuestions;
  }

  if (questions.length === 0) {
    document.getElementById('loading-text').textContent = '문제가 없습니다';
    return;
  }

  currentIndex = Math.min(startIdx, questions.length - 1);

  // Init canvas
  const canvas = document.getElementById('draw-canvas');
  initAnnotation(canvas, async (strokes) => {
    const q = questions[currentIndex];
    if (q) await saveAnnotation(qId(q), strokes);
  });
  setDrawingMode(true);

  // KaTeX
  if (window.renderMathInElement) {
    setKatexReady();
  } else {
    window.addEventListener('katex-ready', () => setKatexReady());
    document.querySelector('script[src*="auto-render"]')
      ?.addEventListener('load', () => setKatexReady());
  }

  document.getElementById('loading').style.display = 'none';
  document.getElementById('app').style.display = 'flex';

  bindEvents();
  showQuestion();
}

// ===========================
// Question Display
// ===========================

async function showQuestion() {
  const q = questions[currentIndex];
  if (!q) return;

  // Load progress
  const progress = await loadProgress(qId(q));
  answered = !!(progress?.answeredAt);
  userAnswer = progress?.userAnswer ?? null;

  // Render question
  const panel = document.getElementById('question-panel');
  panel.innerHTML = renderQuestionCard(q, { answered, userAnswer, progress });
  renderMath(panel);

  // Solution toggle
  const toggle = panel.querySelector('.solution-toggle');
  if (toggle) {
    toggle.addEventListener('click', () => {
      const body = panel.querySelector('.solution-body');
      const expanded = toggle.getAttribute('aria-expanded') === 'true';
      toggle.setAttribute('aria-expanded', !expanded);
      body.style.display = expanded ? 'none' : 'block';
      toggle.querySelector('.chevron').textContent = expanded ? '\u25BC' : '\u25B2';
      renderMath(body);
    });
  }

  // Choice click handlers
  panel.querySelectorAll('.choice-btn').forEach((btn) => {
    btn.addEventListener('click', () => handleChoice(parseInt(btn.dataset.choice)));
  });

  // Update info bar
  document.getElementById('q-info').textContent =
    `${q.subject} | ${q.year}년 ${q.session} Q${q.q_no}  (${currentIndex + 1}/${questions.length})`;

  // Load saved annotation for this question
  const savedStrokes = await loadAnnotation(qId(q));
  loadStrokes(savedStrokes || []);

  // Scroll to top
  panel.scrollTop = 0;
}

async function handleChoice(choiceNum) {
  if (answered) return;
  const q = questions[currentIndex];
  answered = true;
  userAnswer = choiceNum;

  await saveProgress(qId(q), {
    isCorrect: choiceNum === q.answer,
    userAnswer: choiceNum,
  });

  showQuestion();
}

// ===========================
// Navigation
// ===========================

function goNext() {
  if (currentIndex < questions.length - 1) {
    flushSave();
    currentIndex++;
    showQuestion();
  }
}

function goPrev() {
  if (currentIndex > 0) {
    flushSave();
    currentIndex--;
    showQuestion();
  }
}

// ===========================
// Tool Selection
// ===========================

function selectTool(toolName) {
  setTool(toolName);
  document.querySelectorAll('.tool-bar .tool-btn').forEach((btn) => {
    btn.classList.toggle('active', btn.dataset.tool === toolName);
  });
}

// ===========================
// Canvas Resize (drag handle)
// ===========================

function initResize() {
  const handle = document.getElementById('resize-handle');
  const questionPanel = document.getElementById('question-panel');
  let startY = 0;
  let startHeight = 0;

  handle.addEventListener('pointerdown', (e) => {
    e.preventDefault();
    startY = e.clientY;
    startHeight = questionPanel.offsetHeight;
    handle.setPointerCapture(e.pointerId);

    const onMove = (ev) => {
      const diff = ev.clientY - startY;
      const newHeight = Math.max(80, Math.min(window.innerHeight - 150, startHeight + diff));
      questionPanel.style.height = newHeight + 'px';
      resizeCanvas();
    };

    const onUp = () => {
      handle.removeEventListener('pointermove', onMove);
      handle.removeEventListener('pointerup', onUp);
    };

    handle.addEventListener('pointermove', onMove);
    handle.addEventListener('pointerup', onUp);
  });
}

// ===========================
// Full-screen Canvas Toggle
// ===========================

function toggleFullscreen() {
  document.body.classList.toggle('fullscreen-canvas');
  resizeCanvas();
}

// ===========================
// Solution Toggle (top bar button)
// ===========================

function toggleSolution() {
  const btn = document.getElementById('solution-toggle-btn');
  const panel = document.getElementById('question-panel');
  const solSection = panel.querySelector('.solution-body');
  const solToggle = panel.querySelector('.solution-toggle');

  if (!answered) return;

  if (solSection) {
    const visible = solSection.style.display !== 'none';
    solSection.style.display = visible ? 'none' : 'block';
    btn.classList.toggle('active', !visible);
    if (solToggle) {
      solToggle.setAttribute('aria-expanded', !visible);
      solToggle.querySelector('.chevron').textContent = visible ? '\u25BC' : '\u25B2';
    }
    if (!visible) renderMath(solSection);
  }
}

// ===========================
// Event Binding
// ===========================

function bindEvents() {
  // Navigation
  document.getElementById('btn-prev').addEventListener('click', goPrev);
  document.getElementById('btn-next').addEventListener('click', goNext);

  // Tools
  document.querySelectorAll('.tool-bar .tool-btn').forEach((btn) => {
    btn.addEventListener('click', () => selectTool(btn.dataset.tool));
  });

  // Clear canvas
  document.getElementById('btn-clear').addEventListener('click', () => {
    clearStrokes();
  });

  // Grid toggle
  document.getElementById('btn-grid').addEventListener('click', () => {
    document.querySelector('.canvas-panel').classList.toggle('show-grid');
  });

  // Fullscreen toggle
  document.getElementById('btn-fullscreen').addEventListener('click', toggleFullscreen);
  document.querySelector('.back-to-split')?.addEventListener('click', toggleFullscreen);

  // Solution toggle
  document.getElementById('solution-toggle-btn').addEventListener('click', toggleSolution);

  // Back button
  document.getElementById('btn-back').addEventListener('click', () => {
    flushSave();
    window.location.href = 'index.html';
  });

  // Keyboard shortcuts
  document.addEventListener('keydown', (e) => {
    if (e.key === 'ArrowRight') goNext();
    else if (e.key === 'ArrowLeft') goPrev();
  });

  // Resize handle
  initResize();

  // Window resize
  window.addEventListener('resize', resizeCanvas);
}

// ===========================
// Start
// ===========================

document.addEventListener('DOMContentLoaded', init);
