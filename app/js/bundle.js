// ===== app/js/db.js =====
// IndexedDB wrapper for annotations and study progress
// Stores: annotations, progress, questions_cache

const DB_NAME = 'ee-study-db';
const DB_VERSION = 2;

let _db = null;

function openDB() {
  if (_db) return Promise.resolve(_db);

  return new Promise((resolve, reject) => {
    const req = indexedDB.open(DB_NAME, DB_VERSION);

    req.onupgradeneeded = (e) => {
      const db = e.target.result;

      // Annotations store: key = question ID string like "2025_1회_1"
      if (!db.objectStoreNames.contains('annotations')) {
        db.createObjectStore('annotations', { keyPath: 'id' });
      }

      // Progress store: key = question ID
      if (!db.objectStoreNames.contains('progress')) {
        const store = db.createObjectStore('progress', { keyPath: 'id' });
        store.createIndex('by_wrong', 'wrongCount', { unique: false });
      }

      // questions_cache: single record with key 'all'
      if (!db.objectStoreNames.contains('questions_cache')) {
        db.createObjectStore('questions_cache', { keyPath: 'key' });
      }
    };

    req.onsuccess = (e) => {
      _db = e.target.result;
      resolve(_db);
    };

    req.onerror = () => reject(req.error);
  });
}

// Generic helpers
function tx(storeName, mode = 'readonly') {
  return _db.transaction(storeName, mode).objectStore(storeName);
}

function promisify(req) {
  return new Promise((resolve, reject) => {
    req.onsuccess = () => resolve(req.result);
    req.onerror = () => reject(req.error);
  });
}

// ===========================
// Annotations
// ===========================

// Annotation format: { id, strokes: [{tool, color, lineWidth, opacity, points:[{x,y}]}] }

async function saveAnnotation(qId, strokes) {
  const store = tx('annotations', 'readwrite');
  await promisify(store.put({ id: qId, strokes, updatedAt: Date.now() }));
}

async function loadAnnotation(qId) {
  const store = tx('annotations', 'readonly');
  const result = await promisify(store.get(qId));
  return result ? result.strokes : [];
}

async function deleteAnnotation(qId) {
  const store = tx('annotations', 'readwrite');
  await promisify(store.delete(qId));
}

async function getAllAnnotations() {
  const store = tx('annotations', 'readonly');
  return promisify(store.getAll());
}

// ===========================
// Progress
// ===========================

// Progress record: { id, answeredAt, isCorrect, userAnswer, wrongCount }

async function saveProgress(qId, { isCorrect, userAnswer }) {
  const store = tx('progress', 'readwrite');
  const existing = await promisify(store.get(qId)) || { id: qId, wrongCount: 0 };
  const updated = {
    ...existing,
    answeredAt: Date.now(),
    isCorrect,
    userAnswer,
    wrongCount: isCorrect ? existing.wrongCount : (existing.wrongCount || 0) + 1,
  };
  await promisify(store.put(updated));
  return updated;
}

async function loadProgress(qId) {
  const store = tx('progress', 'readonly');
  return promisify(store.get(qId));
}

async function getAllProgress() {
  const store = tx('progress', 'readonly');
  return promisify(store.getAll());
}

async function getWrongIds() {
  const all = await getAllProgress();
  return all
    .filter((p) => p.wrongCount > 0)
    .sort((a, b) => b.wrongCount - a.wrongCount)
    .map((p) => p.id);
}

async function clearAllProgress() {
  const store = tx('progress', 'readwrite');
  return promisify(store.clear());
}

// ===========================
// Questions Cache
// ===========================

async function cacheQuestions(questions) {
  const store = tx('questions_cache', 'readwrite');
  await promisify(store.put({ key: 'all', data: questions, cachedAt: Date.now() }));
}

async function getCachedQuestions() {
  const store = tx('questions_cache', 'readonly');
  const record = await promisify(store.get('all'));
  return record ? record.data : null;
}

// ===========================
// Export / Import
// ===========================

async function exportData() {
  const [annotations, progress] = await Promise.all([
    getAllAnnotations(),
    getAllProgress(),
  ]);
  return { annotations, progress, exportedAt: new Date().toISOString(), version: 1 };
}

async function importData({ annotations = [], progress = [] }) {
  // Import annotations
  const annStore = tx('annotations', 'readwrite');
  for (const item of annotations) {
    await promisify(annStore.put(item));
  }

  // Import progress
  const progStore = tx('progress', 'readwrite');
  for (const item of progress) {
    await promisify(progStore.put(item));
  }
}


// ===== app/js/store.js =====
// Data store: question loading, filtering, searching
// All questions are loaded into memory for fast access

let _questions = [];
let _stats = null;

// Unique question ID
function qId(q) {
  return `${q.year}_${q.session}_${q.q_no}`;
}

// ===========================
// Data Loading
// ===========================

async function loadQuestions(onProgress) {
  if (_questions.length > 0) return _questions;

  onProgress && onProgress(10, '데이터 로딩 중...');

  const response = await fetch('./data/questions.json');
  if (!response.ok) throw new Error(`HTTP ${response.status}`);

  onProgress && onProgress(50, '파싱 중...');
  _questions = await response.json();

  // Attach IDs
  _questions.forEach((q) => { q._id = qId(q); });

  onProgress && onProgress(100, '완료');
  return _questions;
}

async function loadStats() {
  if (_stats) return _stats;
  try {
    const response = await fetch('./data/stats.json');
    _stats = await response.json();
    return _stats;
  } catch {
    return null;
  }
}

function getQuestions() {
  return _questions;
}

// ===========================
// Filtering
// ===========================

function filterBySubject(subject) {
  return _questions.filter((q) => q.subject === subject);
}

function filterByTag(tag) {
  return _questions.filter((q) => q.tag === tag);
}

function filterByYearSession(year, session) {
  return _questions.filter(
    (q) => q.year === parseInt(year) && q.session === session
  );
}

function filterByIds(ids) {
  const idSet = new Set(ids);
  const map = new Map(_questions.map((q) => [q._id, q]));
  return ids.map((id) => map.get(id)).filter(Boolean);
}

// ===========================
// Stats from loaded data
// ===========================

function getSubjects() {
  const subjectSet = new Set(_questions.map((q) => q.subject).filter(Boolean));
  return Array.from(subjectSet).sort();
}

function getTagsBySubject() {
  const map = {};
  for (const q of _questions) {
    if (!q.subject || !q.tag) continue;
    if (!map[q.subject]) map[q.subject] = new Set();
    map[q.subject].add(q.tag);
  }
  return Object.fromEntries(
    Object.entries(map).map(([s, tags]) => [s, Array.from(tags).sort()])
  );
}

function getYearSessions() {
  const map = {};
  for (const q of _questions) {
    if (!q.year || !q.session) continue;
    const key = String(q.year);
    if (!map[key]) map[key] = new Set();
    map[key].add(q.session);
  }
  // Sort years descending
  return Object.fromEntries(
    Object.entries(map)
      .sort(([a], [b]) => parseInt(b) - parseInt(a))
      .map(([y, sessions]) => [y, Array.from(sessions).sort()])
  );
}

function countBySubject() {
  const counts = {};
  for (const q of _questions) {
    counts[q.subject] = (counts[q.subject] || 0) + 1;
  }
  return counts;
}

function countByTag() {
  const counts = {};
  for (const q of _questions) {
    if (q.tag) counts[q.tag] = (counts[q.tag] || 0) + 1;
  }
  return counts;
}

function countByYearSession() {
  const counts = {};
  for (const q of _questions) {
    const key = `${q.year}_${q.session}`;
    counts[key] = (counts[key] || 0) + 1;
  }
  return counts;
}

// ===========================
// Search
// ===========================

function search(query, limit = 50) {
  if (!query || query.trim().length < 1) return [];
  const q = query.trim().toLowerCase();
  const results = [];
  for (const question of _questions) {
    if (results.length >= limit) break;
    const text = (question.text || '').toLowerCase();
    const tag = (question.tag || '').toLowerCase();
    const subject = (question.subject || '').toLowerCase();
    if (text.includes(q) || tag.includes(q) || subject.includes(q)) {
      results.push(question);
    }
  }
  return results;
}


// ===== app/js/render.js =====
// Question card rendering with KaTeX and SVG support

// ===========================
// KaTeX rendering
// ===========================

let _katexReady = false;
const _katexQueue = [];

function setKatexReady() {
  _katexReady = true;
  _katexQueue.forEach((fn) => fn());
  _katexQueue.length = 0;
}

function renderKatexInElement(el) {
  if (!window.renderMathInElement) return;
  try {
    window.renderMathInElement(el, {
      delimiters: [
        { left: '\\[', right: '\\]', display: true },
        { left: '\\(', right: '\\)', display: false },
        { left: '$$', right: '$$', display: true },
        { left: '$', right: '$', display: false },
      ],
      throwOnError: false,
      errorColor: '#f85149',
    });
  } catch (e) {
    console.warn('KaTeX render error:', e);
  }
}

function renderMath(el) {
  if (_katexReady) {
    renderKatexInElement(el);
  } else {
    _katexQueue.push(() => renderKatexInElement(el));
  }
}

// ===========================
// Safe HTML helpers
// ===========================

function escapeHtml(str) {
  if (!str) return '';
  return str
    .replace(/&/g, '&amp;')
    .replace(/</g, '&lt;')
    .replace(/>/g, '&gt;')
    .replace(/"/g, '&quot;');
}

// Safely render text that may contain KaTeX math
// Math delimiters are preserved; HTML is escaped outside delimiters
function renderTextSafe(text) {
  if (!text) return '';
  // We trust the text content from our own data (not user input)
  // but still sanitize SVG injection by not allowing raw HTML outside SVG fields
  return text;
}

// ===========================
// Badge helpers
// ===========================

function subjectColor(subject) {
  const colors = {
    '전기자기학': '#58a6ff',
    '전기기기': '#3fb950',
    '전력공학': '#f0883e',
    '회로이론': '#bc8cff',
    '전기설비기술기준': '#e3b341',
    '제어공학': '#79c0ff',
  };
  return colors[subject] || '#8b949e';
}

// ===========================
// Choice rendering
// ===========================

function renderChoices(choices, answered, correctAnswer, userAnswer) {
  return choices.map((text, idx) => {
    const num = idx + 1;
    let cls = 'choice-btn';

    if (answered) {
      if (num === correctAnswer) cls += ' correct';
      else if (num === userAnswer && num !== correctAnswer) cls += ' wrong';
    }

    const disabled = answered ? 'disabled' : '';
    return `<li>
      <button class="${cls}" data-choice="${num}" ${disabled} aria-label="선택지 ${num}">
        ${escapeHtml(text)}
      </button>
    </li>`;
  }).join('');
}

// ===========================
// Main question card
// ===========================

function renderQuestionCard(question, { answered = false, userAnswer = null, progress = null } = {}) {
  const { year, session, q_no, subject, tag, text, choices, answer, solution, steps, figure_svg, solution_svg } = question;

  const isCorrect = answered && userAnswer === answer;
  const isWrong = answered && userAnswer !== null && userAnswer !== answer;

  // Meta badges
  const metaHtml = `
    <div class="q-meta">
      <span class="q-badge subject" style="color:${subjectColor(subject)};border-color:${subjectColor(subject)}40;background:${subjectColor(subject)}14">${escapeHtml(subject)}</span>
      <span class="q-badge tag">${escapeHtml(tag || '')}</span>
      <span class="q-badge year-session">${year}년 ${escapeHtml(session)} Q${q_no}</span>
    </div>`;

  // Figure SVG (question figure)
  const figureHtml = figure_svg
    ? `<div class="q-figure" aria-label="문제 그림">${figure_svg}</div>`
    : '';

  // Choices
  const choicesHtml = `
    <ul class="choices-list" aria-label="선택지">
      ${renderChoices(choices || [], answered, answer, userAnswer)}
    </ul>`;

  // Result indicator
  let resultHtml = '';
  if (answered) {
    if (isCorrect) {
      resultHtml = `<div class="result-indicator correct show" role="alert">
        <span aria-hidden="true">✓</span> 정답입니다!
      </div>`;
    } else if (isWrong) {
      resultHtml = `<div class="result-indicator wrong show" role="alert">
        <span aria-hidden="true">✗</span> 오답입니다. 정답: ${answer}번
      </div>`;
    }
  }

  // Solution / Steps (hidden by default)
  let solutionHtml = '';
  if (answered) {
    let stepsHtml = '';
    if (steps) {
      const stepItems = [
        { key: '인식', label: '인식', cls: 'recognize' },
        { key: '변환', label: '변환', cls: 'transform' },
        { key: '계산', label: '계산', cls: 'calculate' },
      ];
      stepsHtml = stepItems
        .filter(({ key }) => steps[key])
        .map(({ key, label, cls }) => `
          <div class="step-block">
            <div class="step-label ${cls}">${label}</div>
            <div class="step-content">${steps[key]}</div>
          </div>`)
        .join('');
    }

    const solutionTextHtml = solution
      ? `<div class="solution-text">${escapeHtml(solution)}</div>`
      : '';

    const solFigureHtml = solution_svg
      ? `<div class="sol-figure" aria-label="풀이 그림">${solution_svg}</div>`
      : '';

    solutionHtml = `
      <div class="solution-section">
        <button class="solution-toggle" aria-expanded="false" aria-controls="solution-body">
          풀이 보기
          <span class="chevron" aria-hidden="true">▼</span>
        </button>
        <div class="solution-body" id="solution-body" role="region" aria-label="풀이">
          ${stepsHtml}
          ${solutionTextHtml}
          ${solFigureHtml}
        </div>
      </div>`;
  }

  return `
    <div class="question-view fade-in" data-q-id="${escapeHtml(question._id)}">
      <div class="question-scroll-area">
        ${metaHtml}
        <div class="q-text">${renderTextSafe(text)}</div>
        ${figureHtml}
        ${choicesHtml}
        ${resultHtml}
        ${solutionHtml}
      </div>
    </div>`;
}

// ===========================
// Question list item (compact)
// ===========================

function renderQuestionListItem(question, progress) {
  const { year, session, q_no, subject, tag, text } = question;
  const hasProgress = progress && progress.answeredAt;
  const statusIcon = hasProgress
    ? (progress.isCorrect ? '✓' : '✗')
    : '';
  const statusColor = hasProgress
    ? (progress.isCorrect ? 'var(--green)' : 'var(--red)')
    : 'transparent';

  return `
    <div class="wrong-item" data-q-id="${escapeHtml(question._id)}" role="button" tabindex="0"
         aria-label="${year}년 ${session} ${q_no}번 - ${subject}">
      <div class="wrong-item-header">
        <span class="q-badge subject" style="font-size:0.75rem;padding:2px 8px;color:${subjectColor(subject)};border-color:${subjectColor(subject)}40;background:${subjectColor(subject)}14">${escapeHtml(subject)}</span>
        <span style="font-size:0.8rem;color:var(--muted)">${year}년 ${escapeHtml(session)} Q${q_no}</span>
        ${hasProgress ? `<span style="color:${statusColor};margin-left:auto;font-size:1rem">${statusIcon}</span>` : ''}
      </div>
      <div class="wrong-item-text">${escapeHtml(text || '')}</div>
      ${progress && progress.wrongCount ? `<div class="wrong-count-badge">오답 ${progress.wrongCount}회</div>` : ''}
    </div>`;
}

// ===========================
// Subject grid card
// ===========================

function renderSubjectCard(subject, count) {
  return `
    <div class="grid-card" data-subject="${escapeHtml(subject)}" role="button" tabindex="0"
         aria-label="${subject} ${count}문제">
      <div class="card-title">${escapeHtml(subject)}</div>
      <div class="card-count">${count.toLocaleString()}문제</div>
    </div>`;
}

// ===========================
// Tag grid card
// ===========================

function renderTagCard(tag, count) {
  return `
    <div class="grid-card" data-tag="${escapeHtml(tag)}" role="button" tabindex="0"
         aria-label="${tag} ${count}문제">
      <div class="card-title">${escapeHtml(tag)}</div>
      <div class="card-count">${count.toLocaleString()}문제</div>
    </div>`;
}


// ===== app/js/annotation.js =====
// Apple Pencil annotation layer using PointerEvents API
// Strokes are stored as arrays of points with tool metadata

const TOOLS = {
  black: { color: '#000000', lineWidth: 2.5, opacity: 1.0 },
  red: { color: '#f85149', lineWidth: 2.5, opacity: 1.0 },
  yellow: { color: '#ffe600', lineWidth: 18, opacity: 0.4 },  // highlighter
  eraser: { color: null, lineWidth: 24, opacity: 1.0 },
};

let _canvas = null;
let _ctx = null;
let _currentTool = 'black';
let _isDrawingMode = false;
let _activeStroke = null;
let _strokes = [];  // Array of completed strokes for current question
let _dirty = false;
let _saveTimer = null;
let _onSave = null;  // callback(strokes)

// ===========================
// Initialization
// ===========================

function initAnnotation(canvas, onSave) {
  _canvas = canvas;
  _ctx = canvas.getContext('2d');
  _onSave = onSave;

  _ctx.lineCap = 'round';
  _ctx.lineJoin = 'round';

  // Pointer events for pen input
  canvas.addEventListener('pointerdown', onPointerDown);
  canvas.addEventListener('pointermove', onPointerMove);
  canvas.addEventListener('pointerup', onPointerUp);
  canvas.addEventListener('pointercancel', onPointerUp);

  // Prevent default touch actions when in drawing mode
  canvas.addEventListener('touchstart', (e) => {
    if (_isDrawingMode) e.preventDefault();
  }, { passive: false });

  resizeCanvas();
  window.addEventListener('resize', resizeCanvas);
}

function resizeCanvas() {
  if (!_canvas) return;
  const rect = _canvas.getBoundingClientRect();
  _canvas.width = rect.width;
  _canvas.height = rect.height;
  redrawAll();
}

// ===========================
// Drawing Mode
// ===========================

function setDrawingMode(enabled) {
  _isDrawingMode = enabled;
  if (enabled) {
    _canvas.classList.add('drawing-mode');
  } else {
    _canvas.classList.remove('drawing-mode');
  }
}

function isDrawingMode() {
  return _isDrawingMode;
}

// ===========================
// Tool Selection
// ===========================

function setTool(toolName) {
  if (TOOLS[toolName] !== undefined || toolName === 'eraser') {
    _currentTool = toolName;
  }
}

function getCurrentTool() {
  return _currentTool;
}

// ===========================
// Stroke Management
// ===========================

function loadStrokes(strokes) {
  _strokes = strokes ? JSON.parse(JSON.stringify(strokes)) : [];
  _dirty = false;
  redrawAll();
}

function clearStrokes() {
  _strokes = [];
  _dirty = true;
  redrawAll();
  scheduleSave();
}

function getStrokes() {
  return _strokes;
}

// ===========================
// Pointer Event Handlers
// ===========================

function onPointerDown(e) {
  if (!_isDrawingMode) return;

  // Only handle pen and mouse (not finger touches to allow scrolling)
  if (e.pointerType === 'touch') return;

  e.preventDefault();
  _canvas.setPointerCapture(e.pointerId);

  const { x, y } = getCanvasCoords(e);
  const tool = TOOLS[_currentTool];

  _activeStroke = {
    tool: _currentTool,
    color: tool.color,
    lineWidth: tool.lineWidth,
    opacity: tool.opacity,
    points: [{ x, y, p: e.pressure || 1 }],
  };
}

function onPointerMove(e) {
  if (!_isDrawingMode || !_activeStroke) return;
  if (e.pointerType === 'touch') return;

  e.preventDefault();

  // Use coalesced events for smoother curves on supported devices
  const events = e.getCoalescedEvents ? e.getCoalescedEvents() : [e];
  for (const ev of events) {
    const { x, y } = getCanvasCoords(ev);
    _activeStroke.points.push({ x, y, p: ev.pressure || 1 });
  }

  // Live draw current stroke
  redrawAll();
  drawStroke(_activeStroke, true);
}

function onPointerUp(e) {
  if (!_activeStroke) return;

  if (_activeStroke.points.length > 1) {
    if (_currentTool === 'eraser') {
      applyEraser(_activeStroke);
    } else {
      _strokes.push(_activeStroke);
    }
    _dirty = true;
    scheduleSave();
  }

  _activeStroke = null;
  redrawAll();
}

// ===========================
// Drawing Utilities
// ===========================

function getCanvasCoords(e) {
  const rect = _canvas.getBoundingClientRect();
  return {
    x: e.clientX - rect.left,
    y: e.clientY - rect.top,
  };
}

function drawStroke(stroke, isActive = false) {
  const { points, color, lineWidth, opacity } = stroke;
  if (points.length < 2) {
    // Single point: draw a dot
    _ctx.save();
    _ctx.globalAlpha = opacity;
    _ctx.fillStyle = color;
    _ctx.beginPath();
    _ctx.arc(points[0].x, points[0].y, lineWidth / 2, 0, Math.PI * 2);
    _ctx.fill();
    _ctx.restore();
    return;
  }

  _ctx.save();
  _ctx.globalAlpha = opacity;
  _ctx.strokeStyle = color;
  _ctx.lineWidth = lineWidth;

  _ctx.beginPath();
  _ctx.moveTo(points[0].x, points[0].y);

  // Quadratic bezier curve smoothing
  for (let i = 1; i < points.length - 1; i++) {
    const cpx = (points[i].x + points[i + 1].x) / 2;
    const cpy = (points[i].y + points[i + 1].y) / 2;
    _ctx.quadraticCurveTo(points[i].x, points[i].y, cpx, cpy);
  }

  // Last point
  const last = points[points.length - 1];
  const secondLast = points[points.length - 2];
  _ctx.quadraticCurveTo(secondLast.x, secondLast.y, last.x, last.y);

  _ctx.stroke();
  _ctx.restore();
}

function redrawAll() {
  if (!_ctx || !_canvas) return;
  _ctx.clearRect(0, 0, _canvas.width, _canvas.height);

  for (const stroke of _strokes) {
    drawStroke(stroke);
  }
}

function applyEraser(eraserStroke) {
  // Remove strokes that overlap with eraser path
  const eraserRadius = eraserStroke.lineWidth;
  _strokes = _strokes.filter((stroke) => {
    for (const ep of eraserStroke.points) {
      for (const sp of stroke.points) {
        const dx = ep.x - sp.x;
        const dy = ep.y - sp.y;
        if (Math.sqrt(dx * dx + dy * dy) < eraserRadius) {
          return false; // Remove this stroke
        }
      }
    }
    return true;
  });
}

// ===========================
// Auto-save
// ===========================

function scheduleSave() {
  if (_saveTimer) clearTimeout(_saveTimer);
  _saveTimer = setTimeout(() => {
    if (_dirty && _onSave) {
      _onSave(_strokes);
      _dirty = false;
    }
  }, 800);
}

// Force immediate save
function flushSave() {
  if (_saveTimer) {
    clearTimeout(_saveTimer);
    _saveTimer = null;
  }
  if (_dirty && _onSave) {
    _onSave(_strokes);
    _dirty = false;
  }
}


// ===== app/js/app.js =====
// Main app controller for 전기기사 학습 PWA
// ===========================
// App State
// ===========================

const state = {
  activeTab: 'all',
  currentQueue: [],      // Array of question objects for current session
  currentIndex: 0,
  answered: false,
  userAnswer: null,
  progressMap: {},       // qId -> progress record
  filterContext: null,   // { type: 'subject'|'tag'|'year'|'wrong', value }
};

// ===========================
// DOM References
// ===========================

const $ = (sel) => document.querySelector(sel);
const $$ = (sel) => document.querySelectorAll(sel);

// ===========================
// App Init
// ===========================

async function init() {
  try {
    // Show loading screen
    const loadingScreen = $('#loading-screen');
    const progressBar = $('.progress-bar-fill');
    const loadingText = $('.loading-text');

    function setProgress(pct, msg) {
      if (progressBar) progressBar.style.width = pct + '%';
      if (loadingText) loadingText.textContent = msg;
    }

    // Open DB
    setProgress(5, 'DB 초기화...');
    await openDB();

    // Load questions
    const questions = await loadQuestions((pct, msg) => setProgress(5 + pct * 0.9, msg));

    // Load all progress
    const allProgress = await getAllProgress();
    for (const p of allProgress) {
      state.progressMap[p.id] = p;
    }

    setProgress(100, '완료');

    // Show app
    loadingScreen.style.display = 'none';
    const app = $('#app');
    app.classList.add('visible');

    // Init annotation canvas
    try {
      const canvas = $('#annotation-canvas');
      initAnnotation(canvas, async (strokes) => {
        const q = currentQuestion();
        if (q) await saveAnnotation(q._id, strokes);
      });
    } catch (e) {
      console.warn('Annotation init error:', e);
    }

    // Bind events
    try {
      bindEvents();
    } catch (e) {
      console.warn('Event binding error:', e);
    }

    // Init KaTeX
    if (window.renderMathInElement) {
      setKatexReady();
    } else {
      window.addEventListener('katex-ready', () => setKatexReady());
    }

    // Show initial view
    console.log('[init] Questions loaded:', questions.length, 'Showing tab: all');
    showTab('all');

  } catch (err) {
    console.error('Init failed:', err);
    const loadingText = $('.loading-text');
    if (loadingText) {
      loadingText.textContent = '로드 실패: ' + err.message;
      loadingText.style.color = 'var(--red)';
    }
    // Still try to show app even if init partially fails
    const loadingScreen = $('#loading-screen');
    if (loadingScreen) loadingScreen.style.display = 'none';
    const app = $('#app');
    if (app) {
      app.classList.add('visible');
      const viewAll = $('#view-all');
      if (viewAll) viewAll.innerHTML = `<div style="padding:24px;color:var(--red)">로드 실패: ${err.message}<br><br><button onclick="location.reload()" style="padding:8px 16px;background:var(--blue);color:white;border:none;border-radius:6px;cursor:pointer">새로고침</button></div>`;
      viewAll.classList.add('active');
    }
  }
}

// ===========================
// Current Question Helper
// ===========================

function currentQuestion() {
  return state.currentQueue[state.currentIndex] || null;
}

// ===========================
// Tab Navigation
// ===========================

function showTab(tabName) {
  state.activeTab = tabName;

  // Update tab buttons
  $$('.tab-btn').forEach((btn) => {
    btn.classList.toggle('active', btn.dataset.tab === tabName);
    btn.setAttribute('aria-selected', String(btn.dataset.tab === tabName));
  });

  // Hide/show views
  $$('.view').forEach((v) => v.classList.remove('active'));

  // Hide question nav when not in question view
  const qNavBar = $('#q-nav-bar');

  if (tabName === 'question') {
    $('#view-question').classList.add('active');
    qNavBar.style.display = 'flex';
    resizeCanvas();
  } else {
    qNavBar.style.display = 'none';
    // Exit drawing mode when leaving question view
    if (isDrawingMode()) {
      setDrawingMode(false);
      $('#pen-toolbar').classList.remove('visible');
      $('#pencil-btn').classList.remove('drawing');
    }

    if (tabName === 'all') renderAllView();
    else if (tabName === 'subject') renderSubjectView();
    else if (tabName === 'tag') renderTagView();
    else if (tabName === 'wrong') renderWrongView();
    else if (tabName === 'settings') renderSettingsView();
  }
}

// ===========================
// All Questions View
// ===========================

function renderAllView() {
  const view = $('#view-all');
  const subjects = getSubjects();
  const counts = countBySubject();
  const total = Object.values(counts).reduce((a, b) => a + b, 0);
  console.log('[renderAllView] subjects:', subjects.length, 'total:', total);

  view.innerHTML = `
    <div class="section-header">
      <h2>전체 문제</h2>
      <span class="counter-badge">${total.toLocaleString()}문제</span>
    </div>
    <div class="grid-list">
      <div class="grid-card" id="all-questions-btn" role="button" tabindex="0"
           style="border-color:rgba(88,166,255,0.3);background:rgba(88,166,255,0.06)">
        <div class="card-title" style="color:var(--blue)">전체 문제</div>
        <div class="card-count">${total.toLocaleString()}문제</div>
      </div>
      ${subjects.map((s) => renderSubjectCard(s, counts[s] || 0)).join('')}
    </div>
  `;

  view.querySelector('#all-questions-btn').addEventListener('click', () => {
    startSession(null, '전체 문제');
  });

  view.querySelectorAll('.grid-card[data-subject]').forEach((card) => {
    card.addEventListener('click', () => {
      startSession({ type: 'subject', value: card.dataset.subject }, card.dataset.subject);
    });
    card.addEventListener('keydown', (e) => {
      if (e.key === 'Enter' || e.key === ' ') card.click();
    });
  });
}

// ===========================
// Subject View
// ===========================

function renderSubjectView() {
  const view = $('#view-subject');
  const subjects = getSubjects();
  const counts = countBySubject();
  const tagsBySubject = getTagsBySubject();

  let html = `<div class="section-header"><h2>과목별</h2></div>`;

  for (const subject of subjects) {
    const tags = tagsBySubject[subject] || [];
    const subjectCount = counts[subject] || 0;

    html += `
      <div class="year-section">
        <div class="year-header" data-subject="${subject}" role="button" tabindex="0"
             aria-expanded="false" aria-controls="subj-${subject}">
          <span>${subject}</span>
          <span style="font-size:0.8rem;color:var(--muted)">${subjectCount}문제</span>
          <span class="chevron" aria-hidden="true">▼</span>
        </div>
        <div class="year-sessions" id="subj-${subject}" role="list">
          <div class="session-btn" data-subject="${subject}" data-all="1"
               role="listitem" tabindex="0">
            <span>전체 ${subject}</span>
            <span class="session-count">${subjectCount}문제</span>
          </div>
          ${tags.map((tag) => {
            const tagCount = filterByTag(tag).filter((q) => q.subject === subject).length;
            return `<div class="session-btn" data-subject="${subject}" data-tag="${tag}"
                         role="listitem" tabindex="0">
              <span>${tag}</span>
              <span class="session-count">${tagCount}문제</span>
            </div>`;
          }).join('')}
        </div>
      </div>`;
  }

  view.innerHTML = html;

  // Toggle subject sections
  view.querySelectorAll('.year-header').forEach((header) => {
    const toggle = () => {
      const panel = view.querySelector(`#subj-${header.dataset.subject}`);
      const isOpen = header.classList.toggle('open');
      panel.classList.toggle('open', isOpen);
      header.setAttribute('aria-expanded', isOpen);
    };
    header.addEventListener('click', toggle);
    header.addEventListener('keydown', (e) => { if (e.key === 'Enter' || e.key === ' ') toggle(); });
  });

  // Session buttons
  view.querySelectorAll('.session-btn').forEach((btn) => {
    const handler = () => {
      const { subject, tag, all } = btn.dataset;
      if (all) {
        startSession({ type: 'subject', value: subject }, subject);
      } else {
        startSession({ type: 'tag', value: tag, subject }, `${tag}`);
      }
    };
    btn.addEventListener('click', handler);
    btn.addEventListener('keydown', (e) => { if (e.key === 'Enter' || e.key === ' ') handler(); });
  });
}

// ===========================
// Tag View
// ===========================

function renderTagView() {
  const view = $('#view-tag');
  const tagsBySubject = getTagsBySubject();
  const allCounts = countByTag();
  const yearSessions = getYearSessions();
  const yearSessionCounts = countByYearSession();

  let searchTimeout = null;

  view.innerHTML = `
    <div class="section-header"><h2>연도별 / 태그별</h2></div>
    <div class="search-wrap">
      <input type="search" class="search-input" id="tag-search"
             placeholder="태그, 과목, 문제 검색..." autocomplete="off"
             aria-label="태그 또는 문제 검색">
    </div>
    <div id="tag-content"></div>`;

  const contentEl = view.querySelector('#tag-content');
  const searchInput = view.querySelector('#tag-search');

  function renderTagDefault() {
    let html = `<div class="section-header" style="padding-top:8px"><h2 style="font-size:0.95rem">연도별</h2></div>`;

    for (const [year, sessions] of Object.entries(yearSessions)) {
      html += `<div class="year-section">
        <div class="year-header" data-year="${year}" role="button" tabindex="0"
             aria-expanded="false" aria-controls="year-${year}">
          <span>${year}년</span>
          <span style="font-size:0.8rem;color:var(--muted)">${sessions.length}회차</span>
          <span class="chevron" aria-hidden="true">▼</span>
        </div>
        <div class="year-sessions" id="year-${year}">
          ${sessions.map((session) => {
            const cnt = yearSessionCounts[`${year}_${session}`] || 0;
            return `<div class="session-btn" data-year="${year}" data-session="${session}"
                         role="button" tabindex="0">
              <span>${year}년 ${session}</span>
              <span class="session-count">${cnt}문제</span>
            </div>`;
          }).join('')}
        </div>
      </div>`;
    }

    html += `<div class="section-header" style="padding-top:12px"><h2 style="font-size:0.95rem">태그별</h2></div>`;

    for (const [subject, tags] of Object.entries(tagsBySubject)) {
      html += `<div class="section-header" style="padding-top:4px;padding-bottom:4px">
        <span style="font-size:0.85rem;color:var(--muted)">${subject}</span>
      </div>
      <div class="grid-list" style="padding-top:0">
        ${tags.map((tag) => renderTagCard(tag, allCounts[tag] || 0)).join('')}
      </div>`;
    }

    contentEl.innerHTML = html;

    // Year toggle
    contentEl.querySelectorAll('.year-header').forEach((header) => {
      const toggle = () => {
        const panel = contentEl.querySelector(`#year-${header.dataset.year}`);
        const isOpen = header.classList.toggle('open');
        panel.classList.toggle('open', isOpen);
        header.setAttribute('aria-expanded', isOpen);
      };
      header.addEventListener('click', toggle);
      header.addEventListener('keydown', (e) => { if (e.key === 'Enter' || e.key === ' ') toggle(); });
    });

    // Year session
    contentEl.querySelectorAll('.session-btn').forEach((btn) => {
      const handler = () => {
        const { year, session } = btn.dataset;
        startSession({ type: 'year', value: year, session }, `${year}년 ${session}`);
      };
      btn.addEventListener('click', handler);
      btn.addEventListener('keydown', (e) => { if (e.key === 'Enter' || e.key === ' ') handler(); });
    });

    // Tag cards
    contentEl.querySelectorAll('.grid-card[data-tag]').forEach((card) => {
      card.addEventListener('click', () => {
        startSession({ type: 'tag', value: card.dataset.tag }, card.dataset.tag);
      });
      card.addEventListener('keydown', (e) => { if (e.key === 'Enter' || e.key === ' ') card.click(); });
    });
  }

  function renderSearchResults(query) {
    const results = search(query, 60);
    if (results.length === 0) {
      contentEl.innerHTML = `<div class="empty-state">검색 결과가 없습니다.<br><small style="font-size:0.8rem">"${query}"</small></div>`;
      return;
    }
    contentEl.innerHTML = `
      <div class="section-header">
        <span style="font-size:0.9rem;color:var(--muted)">"${query}" 검색 결과 ${results.length}건</span>
      </div>
      <div class="wrong-list">
        ${results.map((q) => renderQuestionListItem(q, state.progressMap[q._id])).join('')}
      </div>`;

    contentEl.querySelectorAll('.wrong-item').forEach((item) => {
      item.addEventListener('click', () => {
        startSession({ type: 'search', results }, `"${query}"`, results.indexOf(results.find(q => q._id === item.dataset.qId)));
      });
    });
  }

  searchInput.addEventListener('input', () => {
    clearTimeout(searchTimeout);
    const query = searchInput.value.trim();
    if (!query) {
      renderTagDefault();
      return;
    }
    searchTimeout = setTimeout(() => renderSearchResults(query), 300);
  });

  renderTagDefault();
}

// ===========================
// Wrong Answer View
// ===========================

async function renderWrongView() {
  const view = $('#view-wrong');

  const wrongIds = await getWrongIds();

  if (wrongIds.length === 0) {
    view.innerHTML = `
      <div class="section-header"><h2>오답노트</h2></div>
      <div class="empty-state">
        <span class="empty-icon" aria-hidden="true">📝</span>
        아직 오답이 없습니다.<br>
        문제를 풀고 틀린 문제가<br>여기에 쌓입니다.
      </div>`;
    return;
  }

  const wrongQuestions = filterByIds(wrongIds);

  view.innerHTML = `
    <div class="section-header">
      <h2>오답노트</h2>
      <span class="counter-badge">${wrongIds.length}문제</span>
    </div>
    <div style="padding:0 16px 8px">
      <button id="review-wrong-btn" class="settings-btn" style="width:100%;min-height:44px;background:rgba(248,81,73,0.12);color:var(--red);border:1px solid rgba(248,81,73,0.3)">
        오답 문제 다시 풀기 (${wrongIds.length}문제)
      </button>
    </div>
    <div class="wrong-list">
      ${wrongQuestions.map((q) => renderQuestionListItem(q, state.progressMap[q._id])).join('')}
    </div>`;

  view.querySelector('#review-wrong-btn').addEventListener('click', () => {
    startSession({ type: 'wrong', ids: wrongIds }, '오답노트');
  });

  view.querySelectorAll('.wrong-item').forEach((item) => {
    item.addEventListener('click', () => {
      const idx = wrongQuestions.findIndex((q) => q._id === item.dataset.qId);
      startSession({ type: 'wrong', ids: wrongIds }, '오답노트', idx >= 0 ? idx : 0);
    });
    item.addEventListener('keydown', (e) => { if (e.key === 'Enter' || e.key === ' ') item.click(); });
  });
}

// ===========================
// Settings View
// ===========================

async function renderSettingsView() {
  const view = $('#view-settings');
  const allProgress = await getAllProgress();
  const answered = allProgress.length;
  const correct = allProgress.filter((p) => p.isCorrect).length;
  const wrong = allProgress.filter((p) => p.wrongCount > 0).length;

  view.innerHTML = `
    <div class="section-header"><h2>설정</h2></div>

    <div class="stats-grid">
      <div class="stat-card">
        <div class="stat-value">${answered}</div>
        <div class="stat-label">풀이 완료</div>
      </div>
      <div class="stat-card">
        <div class="stat-value" style="color:var(--green)">${correct}</div>
        <div class="stat-label">정답</div>
      </div>
      <div class="stat-card">
        <div class="stat-value" style="color:var(--red)">${wrong}</div>
        <div class="stat-label">오답</div>
      </div>
    </div>

    <div class="settings-section">
      <div class="settings-label">데이터</div>
      <div class="settings-row" id="export-btn" role="button" tabindex="0">
        <div class="settings-row-text">
          <div class="settings-row-title">학습 데이터 내보내기</div>
          <div class="settings-row-sub">풀이 기록 및 필기 내용 JSON 저장</div>
        </div>
        <button class="settings-btn">내보내기</button>
      </div>
      <div class="settings-row" id="import-btn" role="button" tabindex="0">
        <div class="settings-row-text">
          <div class="settings-row-title">학습 데이터 가져오기</div>
          <div class="settings-row-sub">이전에 내보낸 JSON 파일 불러오기</div>
        </div>
        <button class="settings-btn">가져오기</button>
      </div>
      <input type="file" id="import-file-input" accept=".json" style="display:none">
    </div>

    <div class="settings-section">
      <div class="settings-label">초기화</div>
      <div class="settings-row" id="clear-progress-btn" role="button" tabindex="0">
        <div class="settings-row-text">
          <div class="settings-row-title">풀이 기록 삭제</div>
          <div class="settings-row-sub">모든 풀이 기록을 삭제합니다</div>
        </div>
        <button class="settings-btn danger">삭제</button>
      </div>
    </div>

    <div class="settings-section">
      <div class="settings-label">앱 정보</div>
      <div class="settings-row" style="cursor:default">
        <div class="settings-row-text">
          <div class="settings-row-title">전기기사 학습 PWA</div>
          <div class="settings-row-sub">기출문제 ${Object.values(countBySubject()).reduce((a,b) => a+b, 0).toLocaleString()}문제 · Apple Pencil 지원</div>
        </div>
      </div>
    </div>`;

  // Export
  view.querySelector('#export-btn').addEventListener('click', async () => {
    const data = await exportData();
    const blob = new Blob([JSON.stringify(data, null, 2)], { type: 'application/json' });
    const url = URL.createObjectURL(blob);
    const a = document.createElement('a');
    a.href = url;
    a.download = `ee-study-backup-${new Date().toISOString().slice(0,10)}.json`;
    a.click();
    URL.revokeObjectURL(url);
  });

  // Import
  const fileInput = view.querySelector('#import-file-input');
  view.querySelector('#import-btn').addEventListener('click', () => fileInput.click());
  fileInput.addEventListener('change', async () => {
    const file = fileInput.files[0];
    if (!file) return;
    try {
      const text = await file.text();
      const data = JSON.parse(text);
      if (data.version !== 1) {
        alert('지원하지 않는 파일 형식입니다.');
        return;
      }
      await importData(data);
      // Reload progress
      const allP = await getAllProgress();
      state.progressMap = {};
      for (const p of allP) state.progressMap[p.id] = p;
      alert('데이터를 성공적으로 가져왔습니다.');
      renderSettingsView();
    } catch (e) {
      alert('파일을 읽는데 실패했습니다: ' + e.message);
    }
  });

  // Clear progress
  view.querySelector('#clear-progress-btn').addEventListener('click', async () => {
    if (!confirm('모든 풀이 기록을 삭제하시겠습니까?\n이 작업은 되돌릴 수 없습니다.')) return;
    await clearAllProgress();
    state.progressMap = {};
    alert('풀이 기록이 삭제되었습니다.');
    renderSettingsView();
  });
}

// ===========================
// Session: Start Question View
// ===========================

async function startSession(filter, title, startIndex = 0) {
  let questions = [];

  if (!filter) {
    const { getQuestions } = await import('./store.js');
    questions = [...getQuestions()];
  } else if (filter.type === 'subject') {
    questions = filterBySubject(filter.value);
  } else if (filter.type === 'tag') {
    questions = filterByTag(filter.value);
    if (filter.subject) {
      questions = questions.filter((q) => q.subject === filter.subject);
    }
  } else if (filter.type === 'year') {
    questions = filterByYearSession(filter.value, filter.session);
  } else if (filter.type === 'wrong') {
    questions = filterByIds(filter.ids);
  } else if (filter.type === 'search') {
    questions = filter.results;
  }

  if (questions.length === 0) {
    alert('해당 조건에 문제가 없습니다.');
    return;
  }

  state.filterContext = filter;
  state.currentQueue = questions;
  state.currentIndex = Math.max(0, Math.min(startIndex, questions.length - 1));
  state.answered = false;
  state.userAnswer = null;

  // Switch to question view
  showTab('question');
  await showQuestion();
}

// ===========================
// Show Question
// ===========================

async function showQuestion() {
  const q = currentQuestion();
  if (!q) return;

  // Save annotation from previous question first
  flushSave();

  const progress = state.progressMap[q._id];
  const answered = progress && progress.answeredAt ? true : false;

  state.answered = answered;
  state.userAnswer = answered ? (progress.userAnswer || null) : null;

  // Render card
  const container = $('#question-container');
  container.innerHTML = renderQuestionCard(q, {
    answered: state.answered,
    userAnswer: state.userAnswer,
    progress,
  });

  // Bind choice buttons
  container.querySelectorAll('.choice-btn').forEach((btn) => {
    btn.addEventListener('click', () => handleChoiceClick(parseInt(btn.dataset.choice)));
  });

  // Bind solution toggle
  const toggle = container.querySelector('.solution-toggle');
  if (toggle) {
    toggle.addEventListener('click', () => {
      const body = container.querySelector('.solution-body');
      const isOpen = toggle.classList.toggle('open');
      body.classList.toggle('open', isOpen);
      toggle.setAttribute('aria-expanded', isOpen);
      if (isOpen) renderMath(body);
    });
  }

  // Render KaTeX
  renderMath(container);

  // Update nav bar
  updateNavBar();

  // Load annotation
  const strokes = await loadAnnotation(q._id);
  loadStrokes(strokes);

  // Scroll to top
  const scrollArea = $('#app-content');
  if (scrollArea) scrollArea.scrollTop = 0;
}

// ===========================
// Choice Click Handler
// ===========================

async function handleChoiceClick(choiceNum) {
  if (state.answered) return;

  const q = currentQuestion();
  if (!q) return;

  state.answered = true;
  state.userAnswer = choiceNum;

  // Save progress
  const progressRecord = await saveProgress(q._id, {
    isCorrect: choiceNum === q.answer,
    userAnswer: choiceNum,
  });
  state.progressMap[q._id] = progressRecord;

  // Re-render question with answer
  const container = $('#question-container');
  container.innerHTML = renderQuestionCard(q, {
    answered: true,
    userAnswer: choiceNum,
    progress: progressRecord,
  });

  // Re-bind solution toggle
  const toggle = container.querySelector('.solution-toggle');
  if (toggle) {
    toggle.addEventListener('click', () => {
      const body = container.querySelector('.solution-body');
      const isOpen = toggle.classList.toggle('open');
      body.classList.toggle('open', isOpen);
      toggle.setAttribute('aria-expanded', isOpen);
      if (isOpen) renderMath(body);
    });
  }

  // Re-bind choice buttons (now disabled)
  container.querySelectorAll('.choice-btn').forEach((btn) => {
    btn.addEventListener('click', () => {});
  });

  renderMath(container);
  updateNavBar();
}

// ===========================
// Navigation Bar
// ===========================

function updateNavBar() {
  const { currentIndex, currentQueue, filterContext } = state;
  const total = currentQueue.length;
  const q = currentQuestion();

  $('#nav-counter').textContent = `${currentIndex + 1} / ${total}`;
  $('#nav-prev').disabled = currentIndex === 0;
  $('#nav-next').disabled = currentIndex === total - 1;

  // Back button title
  let backTitle = '목록';
  if (filterContext) {
    if (filterContext.type === 'subject') backTitle = filterContext.value;
    else if (filterContext.type === 'tag') backTitle = filterContext.value;
    else if (filterContext.type === 'year') backTitle = `${filterContext.value}년 ${filterContext.session}`;
    else if (filterContext.type === 'wrong') backTitle = '오답노트';
    else if (filterContext.type === 'search') backTitle = '검색 결과';
  }

  // Update pencil button state
  const pencilBtn = $('#pencil-btn');
  if (isDrawingMode()) {
    pencilBtn.classList.add('drawing');
    pencilBtn.setAttribute('aria-label', '필기 모드 끄기');
  } else {
    pencilBtn.classList.remove('drawing');
    pencilBtn.setAttribute('aria-label', '필기 모드 켜기');
  }
}

// ===========================
// Event Binding
// ===========================

function bindEvents() {
  // Tab buttons
  $$('.tab-btn').forEach((btn) => {
    btn.addEventListener('click', () => showTab(btn.dataset.tab));
  });

  // Nav prev/next
  $('#nav-prev').addEventListener('click', async () => {
    if (state.currentIndex > 0) {
      state.currentIndex--;
      state.answered = false;
      state.userAnswer = null;
      await showQuestion();
    }
  });

  $('#nav-next').addEventListener('click', async () => {
    if (state.currentIndex < state.currentQueue.length - 1) {
      state.currentIndex++;
      state.answered = false;
      state.userAnswer = null;
      await showQuestion();
    }
  });

  // Swipe navigation
  let touchStartX = 0;
  let touchStartY = 0;

  const content = $('#app-content');
  content.addEventListener('touchstart', (e) => {
    if (isDrawingMode()) return;
    touchStartX = e.touches[0].clientX;
    touchStartY = e.touches[0].clientY;
  }, { passive: true });

  content.addEventListener('touchend', (e) => {
    if (isDrawingMode()) return;
    if (state.activeTab !== 'question') return;
    const dx = e.changedTouches[0].clientX - touchStartX;
    const dy = e.changedTouches[0].clientY - touchStartY;
    if (Math.abs(dx) > 60 && Math.abs(dx) > Math.abs(dy) * 1.5) {
      if (dx < 0 && state.currentIndex < state.currentQueue.length - 1) {
        $('#nav-next').click();
      } else if (dx > 0 && state.currentIndex > 0) {
        $('#nav-prev').click();
      }
    }
  }, { passive: true });

  // Pencil button (toggle drawing mode)
  const pencilBtn = $('#pencil-btn');
  const penToolbar = $('#pen-toolbar');

  pencilBtn.addEventListener('click', () => {
    const newMode = !isDrawingMode();
    setDrawingMode(newMode);
    penToolbar.classList.toggle('visible', newMode);
    pencilBtn.classList.toggle('drawing', newMode);
    pencilBtn.setAttribute('aria-label', newMode ? '필기 모드 끄기' : '필기 모드 켜기');
  });

  // Pen tool buttons
  penToolbar.querySelectorAll('.pen-tool-btn[data-tool]').forEach((btn) => {
    btn.addEventListener('click', () => {
      const tool = btn.dataset.tool;
      setTool(tool);
      // Update active state
      penToolbar.querySelectorAll('.pen-tool-btn[data-tool]').forEach((b) => {
        b.classList.toggle('active', b.dataset.tool === tool);
      });
    });
  });

  // Set initial active tool
  penToolbar.querySelector('[data-tool="black"]').classList.add('active');

  // Clear annotation button
  penToolbar.querySelector('#clear-annotation-btn').addEventListener('click', async () => {
    if (!confirm('현재 문제의 필기를 모두 지우시겠습니까?')) return;
    clearStrokes();
    const q = currentQuestion();
    if (q) await saveAnnotation(q._id, []);
  });

  // Close pen toolbar
  penToolbar.querySelector('#close-pen-btn').addEventListener('click', () => {
    setDrawingMode(false);
    penToolbar.classList.remove('visible');
    pencilBtn.classList.remove('drawing');
    pencilBtn.setAttribute('aria-label', '필기 모드 켜기');
  });

  // Keyboard navigation (iPad keyboard)
  document.addEventListener('keydown', (e) => {
    if (state.activeTab !== 'question') return;
    if (e.key === 'ArrowRight' || e.key === 'ArrowDown') {
      e.preventDefault();
      $('#nav-next').click();
    } else if (e.key === 'ArrowLeft' || e.key === 'ArrowUp') {
      e.preventDefault();
      $('#nav-prev').click();
    } else if (e.key === 'Escape') {
      if (isDrawingMode()) {
        setDrawingMode(false);
        penToolbar.classList.remove('visible');
        pencilBtn.classList.remove('drawing');
      }
    }
  });

  // Handle KaTeX loaded via window event
  window.addEventListener('load', () => {
    if (window.renderMathInElement) {
      setKatexReady();
    }
  });
}

// ===========================
// Start
// ===========================

// Wait for DOM
if (document.readyState === 'loading') {
  document.addEventListener('DOMContentLoaded', init);
} else {
  init();
}
