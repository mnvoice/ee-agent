// Main app controller for 전기기사 학습 PWA
import {
  loadQuestions, loadStats,
  filterBySubject, filterByTag, filterByYearSession, filterByIds,
  getSubjects, getTagsBySubject, getYearSessions,
  countBySubject, countByTag, countByYearSession,
  search,
} from './store.js';

import {
  renderQuestionCard,
  renderSubjectCard, renderTagCard, renderQuestionListItem,
  setKatexReady, renderMath,
} from './render.js';

import {
  initAnnotation, resizeCanvas, setDrawingMode,
  isDrawingMode, setTool, getCurrentTool,
  loadStrokes, clearStrokes, flushSave, getStrokes,
} from './annotation.js';

import {
  openDB, saveAnnotation, loadAnnotation,
  saveProgress, loadProgress, getAllProgress,
  getWrongIds, clearAllProgress, exportData, importData,
} from './db.js';

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
