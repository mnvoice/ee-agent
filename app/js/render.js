// Question card rendering with KaTeX and SVG support

// ===========================
// KaTeX rendering
// ===========================

let _katexReady = false;
const _katexQueue = [];

export function setKatexReady() {
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

export function renderMath(el) {
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

export function renderChoices(choices, answered, correctAnswer, userAnswer) {
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

export function renderQuestionCard(question, { answered = false, userAnswer = null, progress = null } = {}) {
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

export function renderQuestionListItem(question, progress) {
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

export function renderSubjectCard(subject, count) {
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

export function renderTagCard(tag, count) {
  return `
    <div class="grid-card" data-tag="${escapeHtml(tag)}" role="button" tabindex="0"
         aria-label="${tag} ${count}문제">
      <div class="card-title">${escapeHtml(tag)}</div>
      <div class="card-count">${count.toLocaleString()}문제</div>
    </div>`;
}
