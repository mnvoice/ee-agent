// 전기기사 학습 PWA - Combined App (No ES Modules)
// Merged from: db.js, store.js, render.js, annotation.js, app.js
(function() {
  'use strict';

  var $ = function(sel) { return document.querySelector(sel); };
  var $$ = function(sel) { return document.querySelectorAll(sel); };

  // ================================================================
  // IndexedDB (from db.js)
  // ================================================================

  var DB_NAME = 'ee-study-db';
  var DB_VERSION = 2;
  var _db = null;

  function openDB() {
    if (_db) return Promise.resolve(_db);
    return new Promise(function(resolve, reject) {
      var req = indexedDB.open(DB_NAME, DB_VERSION);
      req.onupgradeneeded = function(e) {
        var db = e.target.result;
        if (!db.objectStoreNames.contains('annotations')) {
          db.createObjectStore('annotations', { keyPath: 'id' });
        }
        if (!db.objectStoreNames.contains('progress')) {
          var store = db.createObjectStore('progress', { keyPath: 'id' });
          store.createIndex('by_wrong', 'wrongCount', { unique: false });
        }
        if (!db.objectStoreNames.contains('questions_cache')) {
          db.createObjectStore('questions_cache', { keyPath: 'key' });
        }
      };
      req.onsuccess = function(e) { _db = e.target.result; resolve(_db); };
      req.onerror = function() { reject(req.error); };
    });
  }

  function tx(storeName, mode) {
    return _db.transaction(storeName, mode || 'readonly').objectStore(storeName);
  }

  function promisify(req) {
    return new Promise(function(resolve, reject) {
      req.onsuccess = function() { resolve(req.result); };
      req.onerror = function() { reject(req.error); };
    });
  }

  function saveAnnotation(qId, strokes) {
    var store = tx('annotations', 'readwrite');
    return promisify(store.put({ id: qId, strokes: strokes, updatedAt: Date.now() }));
  }

  function loadAnnotation(qId) {
    var store = tx('annotations', 'readonly');
    return promisify(store.get(qId)).then(function(r) { return r ? r.strokes : []; });
  }

  function getAllAnnotations() {
    return promisify(tx('annotations', 'readonly').getAll());
  }

  function saveProgress(qId, opts) {
    var store = tx('progress', 'readwrite');
    return promisify(store.get(qId)).then(function(existing) {
      existing = existing || { id: qId, wrongCount: 0 };
      var updated = {
        id: existing.id,
        answeredAt: Date.now(),
        isCorrect: opts.isCorrect,
        userAnswer: opts.userAnswer,
        wrongCount: opts.isCorrect ? existing.wrongCount : (existing.wrongCount || 0) + 1,
      };
      var store2 = tx('progress', 'readwrite');
      return promisify(store2.put(updated)).then(function() { return updated; });
    });
  }

  function getAllProgress() {
    return promisify(tx('progress', 'readonly').getAll());
  }

  function getWrongIds() {
    return getAllProgress().then(function(all) {
      return all
        .filter(function(p) { return p.wrongCount > 0; })
        .sort(function(a, b) { return b.wrongCount - a.wrongCount; })
        .map(function(p) { return p.id; });
    });
  }

  function clearAllProgress() {
    return promisify(tx('progress', 'readwrite').clear());
  }

  function exportData() {
    return Promise.all([getAllAnnotations(), getAllProgress()]).then(function(r) {
      return { annotations: r[0], progress: r[1], exportedAt: new Date().toISOString(), version: 1 };
    });
  }

  function importData(data) {
    var annotations = data.annotations || [];
    var progress = data.progress || [];
    var p = Promise.resolve();
    if (annotations.length > 0) {
      p = p.then(function() {
        var t = _db.transaction('annotations', 'readwrite');
        var s = t.objectStore('annotations');
        annotations.forEach(function(item) { s.put(item); });
        return new Promise(function(resolve, reject) {
          t.oncomplete = resolve;
          t.onerror = function() { reject(t.error); };
        });
      });
    }
    if (progress.length > 0) {
      p = p.then(function() {
        var t = _db.transaction('progress', 'readwrite');
        var s = t.objectStore('progress');
        progress.forEach(function(item) { s.put(item); });
        return new Promise(function(resolve, reject) {
          t.oncomplete = resolve;
          t.onerror = function() { reject(t.error); };
        });
      });
    }
    return p;
  }

  // ================================================================
  // Data Store (from store.js)
  // ================================================================

  var _questions = [];

  function qId(q) {
    return q.year + '_' + q.session + '_' + q.q_no;
  }

  function loadQuestions(onProgress) {
    if (_questions.length > 0) return Promise.resolve(_questions);
    if (onProgress) onProgress(10, '\uB370\uC774\uD130 \uB85C\uB529 \uC911...');
    return fetch('./data/questions.json').then(function(response) {
      if (!response.ok) throw new Error('HTTP ' + response.status);
      if (onProgress) onProgress(50, '\uD30C\uC2F1 \uC911...');
      return response.json();
    }).then(function(data) {
      _questions = data;
      _questions.forEach(function(q) { q._id = qId(q); });
      if (onProgress) onProgress(100, '\uC644\uB8CC');
      return _questions;
    });
  }

  function filterBySubject(subject) {
    return _questions.filter(function(q) { return q.subject === subject; });
  }

  function filterByTag(tag) {
    return _questions.filter(function(q) { return q.tag === tag; });
  }

  function filterByYearSession(year, session) {
    return _questions.filter(function(q) {
      return q.year === parseInt(year) && q.session === session;
    });
  }

  function filterByIds(ids) {
    var map = {};
    _questions.forEach(function(q) { map[q._id] = q; });
    return ids.map(function(id) { return map[id]; }).filter(Boolean);
  }

  function getSubjects() {
    var set = {};
    _questions.forEach(function(q) { if (q.subject) set[q.subject] = 1; });
    return Object.keys(set).sort();
  }

  function getTagsBySubject() {
    var map = {};
    _questions.forEach(function(q) {
      if (!q.subject || !q.tag) return;
      if (!map[q.subject]) map[q.subject] = {};
      map[q.subject][q.tag] = 1;
    });
    var result = {};
    Object.keys(map).sort().forEach(function(s) {
      result[s] = Object.keys(map[s]).sort();
    });
    return result;
  }

  function getYearSessions() {
    var map = {};
    _questions.forEach(function(q) {
      if (!q.year || !q.session) return;
      var key = String(q.year);
      if (!map[key]) map[key] = {};
      map[key][q.session] = 1;
    });
    var entries = Object.keys(map).sort(function(a, b) { return parseInt(b) - parseInt(a); });
    var result = {};
    entries.forEach(function(y) {
      result[y] = Object.keys(map[y]).sort();
    });
    return result;
  }

  function countBySubject() {
    var counts = {};
    _questions.forEach(function(q) { counts[q.subject] = (counts[q.subject] || 0) + 1; });
    return counts;
  }

  function countByTag() {
    var counts = {};
    _questions.forEach(function(q) { if (q.tag) counts[q.tag] = (counts[q.tag] || 0) + 1; });
    return counts;
  }

  function countByYearSession() {
    var counts = {};
    _questions.forEach(function(q) {
      var key = q.year + '_' + q.session;
      counts[key] = (counts[key] || 0) + 1;
    });
    return counts;
  }

  function searchQuestions(query, limit) {
    limit = limit || 50;
    if (!query || query.trim().length < 1) return [];
    var q = query.trim().toLowerCase();
    var results = [];
    for (var i = 0; i < _questions.length && results.length < limit; i++) {
      var question = _questions[i];
      var text = (question.text || '').toLowerCase();
      var tag = (question.tag || '').toLowerCase();
      var subject = (question.subject || '').toLowerCase();
      if (text.indexOf(q) >= 0 || tag.indexOf(q) >= 0 || subject.indexOf(q) >= 0) {
        results.push(question);
      }
    }
    return results;
  }

  // ================================================================
  // Renderer (from render.js)
  // ================================================================

  var _katexReady = false;
  var _katexQueue = [];

  function setKatexReady() {
    _katexReady = true;
    _katexQueue.forEach(function(fn) { fn(); });
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
      _katexQueue.push(function() { renderKatexInElement(el); });
    }
  }

  function escapeHtml(str) {
    if (!str) return '';
    return String(str)
      .replace(/&/g, '&amp;')
      .replace(/</g, '&lt;')
      .replace(/>/g, '&gt;')
      .replace(/"/g, '&quot;');
  }

  function subjectColor(subject) {
    var colors = {
      '\uC804\uAE30\uC790\uAE30\uD559': '#58a6ff',
      '\uC804\uAE30\uAE30\uAE30': '#3fb950',
      '\uC804\uB825\uACF5\uD559': '#f0883e',
      '\uD68C\uB85C\uC774\uB860': '#bc8cff',
      '\uC804\uAE30\uC124\uBE44\uAE30\uC220\uAE30\uC900': '#e3b341',
      '\uC81C\uC5B4\uACF5\uD559': '#79c0ff',
    };
    return colors[subject] || '#8b949e';
  }

  function renderChoices(choices, answered, correctAnswer, userAnswer) {
    return choices.map(function(text, idx) {
      var num = idx + 1;
      var cls = 'choice-btn';
      if (answered) {
        if (num === correctAnswer) cls += ' correct';
        else if (num === userAnswer && num !== correctAnswer) cls += ' wrong';
      }
      var disabled = answered ? 'disabled' : '';
      return '<li><button class="' + cls + '" data-choice="' + num + '" ' + disabled +
        ' aria-label="\uC120\uD0DD\uC9C0 ' + num + '">' + escapeHtml(text) + '</button></li>';
    }).join('');
  }

  function renderQuestionCard(question, opts) {
    opts = opts || {};
    var answered = opts.answered || false;
    var userAnswer = opts.userAnswer || null;
    var progress = opts.progress || null;
    var year = question.year, session = question.session, q_no = question.q_no;
    var subject = question.subject, tag = question.tag, text = question.text;
    var choices = question.choices, answer = question.answer;
    var solution = question.solution, steps = question.steps;
    var figure_svg = question.figure_svg, solution_svg = question.solution_svg;
    var isCorrect = answered && userAnswer === answer;
    var isWrong = answered && userAnswer !== null && userAnswer !== answer;
    var sc = subjectColor(subject);

    var metaHtml = '<div class="q-meta">' +
      '<span class="q-badge subject" style="color:' + sc + ';border-color:' + sc + '40;background:' + sc + '14">' + escapeHtml(subject) + '</span>' +
      '<span class="q-badge tag">' + escapeHtml(tag || '') + '</span>' +
      '<span class="q-badge year-session">' + year + '\uB144 ' + escapeHtml(session) + ' Q' + q_no + '</span>' +
      '</div>';

    var figureHtml = figure_svg
      ? '<div class="q-figure" aria-label="\uBB38\uC81C \uADF8\uB9BC">' + figure_svg + '</div>'
      : '';

    var choicesHtml = '<ul class="choices-list" aria-label="\uC120\uD0DD\uC9C0">' +
      renderChoices(choices || [], answered, answer, userAnswer) + '</ul>';

    var resultHtml = '';
    if (answered) {
      if (isCorrect) {
        resultHtml = '<div class="result-indicator correct show" role="alert"><span aria-hidden="true">\u2713</span> \uC815\uB2F5\uC785\uB2C8\uB2E4!</div>';
      } else if (isWrong) {
        resultHtml = '<div class="result-indicator wrong show" role="alert"><span aria-hidden="true">\u2717</span> \uC624\uB2F5\uC785\uB2C8\uB2E4. \uC815\uB2F5: ' + answer + '\uBC88</div>';
      }
    }

    var solutionHtml = '';
    if (answered) {
      var stepsHtml = '';
      if (steps) {
        var stepItems = [
          { key: '\uC778\uC2DD', label: '\uC778\uC2DD', cls: 'recognize' },
          { key: '\uBCC0\uD658', label: '\uBCC0\uD658', cls: 'transform' },
          { key: '\uACC4\uC0B0', label: '\uACC4\uC0B0', cls: 'calculate' },
        ];
        stepItems.forEach(function(si) {
          if (steps[si.key]) {
            stepsHtml += '<div class="step-block"><div class="step-label ' + si.cls + '">' + si.label +
              '</div><div class="step-content">' + steps[si.key] + '</div></div>';
          }
        });
      }
      var solutionTextHtml = solution ? '<div class="solution-text">' + escapeHtml(solution) + '</div>' : '';
      var solFigureHtml = solution_svg ? '<div class="sol-figure" aria-label="\uD480\uC774 \uADF8\uB9BC">' + solution_svg + '</div>' : '';

      solutionHtml = '<div class="solution-section">' +
        '<button class="solution-toggle" aria-expanded="false" aria-controls="solution-body">' +
        '\uD480\uC774 \uBCF4\uAE30 <span class="chevron" aria-hidden="true">\u25BC</span></button>' +
        '<div class="solution-body" id="solution-body" role="region" aria-label="\uD480\uC774">' +
        stepsHtml + solutionTextHtml + solFigureHtml + '</div></div>';
    }

    return '<div class="question-view fade-in" data-q-id="' + escapeHtml(question._id) + '">' +
      '<div class="question-scroll-area">' +
      metaHtml + '<div class="q-text">' + (text || '') + '</div>' +
      figureHtml + choicesHtml + resultHtml + solutionHtml +
      '</div></div>';
  }

  function renderQuestionListItem(question, progress) {
    var hasProgress = progress && progress.answeredAt;
    var statusIcon = hasProgress ? (progress.isCorrect ? '\u2713' : '\u2717') : '';
    var statusColor = hasProgress ? (progress.isCorrect ? 'var(--green)' : 'var(--red)') : 'transparent';
    var sc = subjectColor(question.subject);

    return '<div class="wrong-item" data-q-id="' + escapeHtml(question._id) + '" role="button" tabindex="0"' +
      ' aria-label="' + question.year + '\uB144 ' + escapeHtml(question.session) + ' ' + question.q_no + '\uBC88 - ' + escapeHtml(question.subject) + '">' +
      '<div class="wrong-item-header">' +
      '<span class="q-badge subject" style="font-size:0.75rem;padding:2px 8px;color:' + sc + ';border-color:' + sc + '40;background:' + sc + '14">' + escapeHtml(question.subject) + '</span>' +
      '<span style="font-size:0.8rem;color:var(--muted)">' + question.year + '\uB144 ' + escapeHtml(question.session) + ' Q' + question.q_no + '</span>' +
      (hasProgress ? '<span style="color:' + statusColor + ';margin-left:auto;font-size:1rem">' + statusIcon + '</span>' : '') +
      '</div>' +
      '<div class="wrong-item-text">' + escapeHtml(question.text || '') + '</div>' +
      (progress && progress.wrongCount ? '<div class="wrong-count-badge">\uC624\uB2F5 ' + progress.wrongCount + '\uD68C</div>' : '') +
      '</div>';
  }

  function renderSubjectCard(subject, count) {
    return '<div class="grid-card" data-subject="' + escapeHtml(subject) + '" role="button" tabindex="0"' +
      ' aria-label="' + escapeHtml(subject) + ' ' + count + '\uBB38\uC81C">' +
      '<div class="card-title">' + escapeHtml(subject) + '</div>' +
      '<div class="card-count">' + count.toLocaleString() + '\uBB38\uC81C</div></div>';
  }

  function renderTagCard(tag, count) {
    return '<div class="grid-card" data-tag="' + escapeHtml(tag) + '" role="button" tabindex="0"' +
      ' aria-label="' + escapeHtml(tag) + ' ' + count + '\uBB38\uC81C">' +
      '<div class="card-title">' + escapeHtml(tag) + '</div>' +
      '<div class="card-count">' + count.toLocaleString() + '\uBB38\uC81C</div></div>';
  }

  // ================================================================
  // Annotation (from annotation.js)
  // ================================================================

  var TOOLS = {
    black: { color: '#000000', lineWidth: 2.5, opacity: 1.0 },
    red: { color: '#f85149', lineWidth: 2.5, opacity: 1.0 },
    yellow: { color: '#ffe600', lineWidth: 18, opacity: 0.4 },
    eraser: { color: null, lineWidth: 24, opacity: 1.0 },
  };

  var _canvas = null;
  var _ctx = null;
  var _currentTool = 'black';
  var _isDrawingMode = false;
  var _activeStroke = null;
  var _strokes = [];
  var _dirty = false;
  var _saveTimer = null;
  var _onSave = null;

  function initAnnotation(canvas, onSave) {
    _canvas = canvas;
    _ctx = canvas.getContext('2d');
    _onSave = onSave;
    _ctx.lineCap = 'round';
    _ctx.lineJoin = 'round';

    canvas.addEventListener('pointerdown', onPointerDown);
    canvas.addEventListener('pointermove', onPointerMove);
    canvas.addEventListener('pointerup', onPointerUp);
    canvas.addEventListener('pointercancel', onPointerUp);
    canvas.addEventListener('touchstart', function(e) {
      if (_isDrawingMode) e.preventDefault();
    }, { passive: false });

    resizeCanvas();
    window.addEventListener('resize', resizeCanvas);
  }

  function resizeCanvas() {
    if (!_canvas) return;
    var rect = _canvas.getBoundingClientRect();
    _canvas.width = rect.width;
    _canvas.height = rect.height;
    redrawAll();
  }

  function setDrawingMode(enabled) {
    _isDrawingMode = enabled;
    if (enabled) _canvas.classList.add('drawing-mode');
    else _canvas.classList.remove('drawing-mode');
  }

  function isDrawingMode() { return _isDrawingMode; }

  function setTool(toolName) {
    if (TOOLS[toolName] !== undefined) _currentTool = toolName;
  }

  function getCurrentTool() { return _currentTool; }

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

  function flushSave() {
    if (_saveTimer) { clearTimeout(_saveTimer); _saveTimer = null; }
    if (_dirty && _onSave) { _onSave(_strokes); _dirty = false; }
  }

  function onPointerDown(e) {
    if (!_isDrawingMode) return;
    if (e.pointerType === 'touch') return;
    e.preventDefault();
    _canvas.setPointerCapture(e.pointerId);
    var coords = getCanvasCoords(e);
    var tool = TOOLS[_currentTool];
    _activeStroke = {
      tool: _currentTool, color: tool.color, lineWidth: tool.lineWidth,
      opacity: tool.opacity, points: [{ x: coords.x, y: coords.y, p: e.pressure || 1 }],
    };
  }

  function onPointerMove(e) {
    if (!_isDrawingMode || !_activeStroke) return;
    if (e.pointerType === 'touch') return;
    e.preventDefault();
    var events = e.getCoalescedEvents ? e.getCoalescedEvents() : [e];
    events.forEach(function(ev) {
      var c = getCanvasCoords(ev);
      _activeStroke.points.push({ x: c.x, y: c.y, p: ev.pressure || 1 });
    });
    redrawAll();
    drawStroke(_activeStroke, true);
  }

  function onPointerUp() {
    if (!_activeStroke) return;
    if (_activeStroke.points.length > 1) {
      if (_currentTool === 'eraser') applyEraser(_activeStroke);
      else _strokes.push(_activeStroke);
      _dirty = true;
      scheduleSave();
    }
    _activeStroke = null;
    redrawAll();
  }

  function getCanvasCoords(e) {
    var rect = _canvas.getBoundingClientRect();
    return { x: e.clientX - rect.left, y: e.clientY - rect.top };
  }

  function drawStroke(stroke) {
    var pts = stroke.points;
    if (pts.length < 2) {
      _ctx.save();
      _ctx.globalAlpha = stroke.opacity;
      _ctx.fillStyle = stroke.color;
      _ctx.beginPath();
      _ctx.arc(pts[0].x, pts[0].y, stroke.lineWidth / 2, 0, Math.PI * 2);
      _ctx.fill();
      _ctx.restore();
      return;
    }
    _ctx.save();
    _ctx.globalAlpha = stroke.opacity;
    _ctx.strokeStyle = stroke.color;
    _ctx.lineWidth = stroke.lineWidth;
    _ctx.beginPath();
    _ctx.moveTo(pts[0].x, pts[0].y);
    for (var i = 1; i < pts.length - 1; i++) {
      var cpx = (pts[i].x + pts[i + 1].x) / 2;
      var cpy = (pts[i].y + pts[i + 1].y) / 2;
      _ctx.quadraticCurveTo(pts[i].x, pts[i].y, cpx, cpy);
    }
    var last = pts[pts.length - 1];
    var secondLast = pts[pts.length - 2];
    _ctx.quadraticCurveTo(secondLast.x, secondLast.y, last.x, last.y);
    _ctx.stroke();
    _ctx.restore();
  }

  function redrawAll() {
    if (!_ctx || !_canvas) return;
    _ctx.clearRect(0, 0, _canvas.width, _canvas.height);
    _strokes.forEach(function(s) { drawStroke(s); });
  }

  function applyEraser(eraserStroke) {
    var r = eraserStroke.lineWidth;
    _strokes = _strokes.filter(function(stroke) {
      for (var i = 0; i < eraserStroke.points.length; i++) {
        var ep = eraserStroke.points[i];
        for (var j = 0; j < stroke.points.length; j++) {
          var sp = stroke.points[j];
          var dx = ep.x - sp.x, dy = ep.y - sp.y;
          if (Math.sqrt(dx * dx + dy * dy) < r) return false;
        }
      }
      return true;
    });
  }

  function scheduleSave() {
    if (_saveTimer) clearTimeout(_saveTimer);
    _saveTimer = setTimeout(function() {
      if (_dirty && _onSave) { _onSave(_strokes); _dirty = false; }
    }, 800);
  }

  // ================================================================
  // App State
  // ================================================================

  var state = {
    activeTab: 'all',
    currentQueue: [],
    currentIndex: 0,
    answered: false,
    userAnswer: null,
    progressMap: {},
    filterContext: null,
  };

  // ================================================================
  // App Init
  // ================================================================

  function init() {
    var loadingScreen = $('#loading-screen');
    var progressBar = $('.progress-bar-fill');
    var loadingText = $('.loading-text');

    function setProgress(pct, msg) {
      if (progressBar) progressBar.style.width = pct + '%';
      if (loadingText) loadingText.textContent = msg;
    }

    setProgress(5, 'DB \uCD08\uAE30\uD654...');

    openDB().then(function() {
      return loadQuestions(function(pct, msg) { setProgress(5 + pct * 0.9, msg); });
    }).then(function() {
      return getAllProgress();
    }).then(function(allProgress) {
      allProgress.forEach(function(p) { state.progressMap[p.id] = p; });
      setProgress(100, '\uC644\uB8CC');

      loadingScreen.style.display = 'none';
      $('#app').classList.add('visible');

      // Init annotation
      try {
        initAnnotation($('#annotation-canvas'), function(strokes) {
          var q = currentQuestion();
          if (q) saveAnnotation(q._id, strokes);
        });
      } catch (e) { console.warn('Annotation init error:', e); }

      // Bind events
      try { bindEvents(); } catch (e) { console.warn('Event binding error:', e); }

      // KaTeX
      if (window.renderMathInElement) {
        setKatexReady();
      }
      window.addEventListener('load', function() {
        if (window.renderMathInElement && !_katexReady) setKatexReady();
      });

      // Show initial view
      showTab('all');
    }).catch(function(err) {
      console.error('Init failed:', err);
      if (loadingText) {
        loadingText.textContent = '\uB85C\uB4DC \uC2E4\uD328: ' + err.message;
        loadingText.style.color = 'var(--red)';
      }
      loadingScreen.style.display = 'none';
      var app = $('#app');
      if (app) {
        app.classList.add('visible');
        var viewAll = $('#view-all');
        if (viewAll) {
          viewAll.innerHTML = '<div style="padding:24px;color:var(--red)">\uB85C\uB4DC \uC2E4\uD328: ' +
            escapeHtml(err.message) + '<br><br><button onclick="location.reload()" ' +
            'style="padding:8px 16px;background:var(--blue);color:white;border:none;border-radius:6px;cursor:pointer">' +
            '\uC0C8\uB85C\uACE0\uCE68</button></div>';
        }
        viewAll.classList.add('active');
      }
    });
  }

  function currentQuestion() {
    return state.currentQueue[state.currentIndex] || null;
  }

  // ================================================================
  // Tab Navigation
  // ================================================================

  function showTab(tabName) {
    state.activeTab = tabName;

    $$('.tab-btn').forEach(function(btn) {
      btn.classList.toggle('active', btn.dataset.tab === tabName);
    });

    $$('.view').forEach(function(v) { v.classList.remove('active'); });

    var qNavBar = $('#q-nav-bar');

    if (tabName === 'question') {
      $('#view-question').classList.add('active');
      qNavBar.style.display = 'flex';
      resizeCanvas();
    } else {
      qNavBar.style.display = 'none';
      if (isDrawingMode()) {
        setDrawingMode(false);
        $('#pen-toolbar').classList.remove('visible');
        $('#pencil-btn').classList.remove('drawing');
      }

      var viewEl = $('#view-' + tabName);
      if (viewEl) viewEl.classList.add('active');

      if (tabName === 'all') renderAllView();
      else if (tabName === 'subject') renderSubjectView();
      else if (tabName === 'tag') renderTagView();
      else if (tabName === 'wrong') renderWrongView();
      else if (tabName === 'settings') renderSettingsView();
    }
  }

  // ================================================================
  // All Questions View
  // ================================================================

  function renderAllView() {
    var view = $('#view-all');
    var subjects = getSubjects();
    var counts = countBySubject();
    var total = 0;
    Object.keys(counts).forEach(function(k) { total += counts[k]; });

    view.innerHTML =
      '<div class="section-header"><h2>\uC804\uCCB4 \uBB38\uC81C</h2>' +
      '<span class="counter-badge">' + total.toLocaleString() + '\uBB38\uC81C</span></div>' +
      '<div class="grid-list">' +
      '<div class="grid-card" id="all-questions-btn" role="button" tabindex="0"' +
      ' style="border-color:rgba(88,166,255,0.3);background:rgba(88,166,255,0.06)">' +
      '<div class="card-title" style="color:var(--blue)">\uC804\uCCB4 \uBB38\uC81C</div>' +
      '<div class="card-count">' + total.toLocaleString() + '\uBB38\uC81C</div></div>' +
      subjects.map(function(s) { return renderSubjectCard(s, counts[s] || 0); }).join('') +
      '</div>';

    view.querySelector('#all-questions-btn').addEventListener('click', function() {
      startSession(null, '\uC804\uCCB4 \uBB38\uC81C');
    });

    view.querySelectorAll('.grid-card[data-subject]').forEach(function(card) {
      card.addEventListener('click', function() {
        startSession({ type: 'subject', value: card.dataset.subject }, card.dataset.subject);
      });
    });
  }

  // ================================================================
  // Subject View
  // ================================================================

  function renderSubjectView() {
    var view = $('#view-subject');
    var subjects = getSubjects();
    var counts = countBySubject();
    var tagsBySubj = getTagsBySubject();

    var html = '<div class="section-header"><h2>\uACFC\uBAA9\uBCC4</h2></div>';

    subjects.forEach(function(subject) {
      var tags = tagsBySubj[subject] || [];
      var subjectCount = counts[subject] || 0;
      var safeId = subject.replace(/[^a-zA-Z0-9\uAC00-\uD7AF]/g, '_');

      html += '<div class="year-section">' +
        '<div class="year-header" data-subject="' + escapeHtml(subject) + '" data-safe-id="' + safeId + '" role="button" tabindex="0">' +
        '<span>' + escapeHtml(subject) + '</span>' +
        '<span style="font-size:0.8rem;color:var(--muted)">' + subjectCount + '\uBB38\uC81C</span>' +
        '<span class="chevron" aria-hidden="true">\u25BC</span></div>' +
        '<div class="year-sessions" id="subj-' + safeId + '">' +
        '<div class="session-btn" data-subject="' + escapeHtml(subject) + '" data-all="1" role="listitem" tabindex="0">' +
        '<span>\uC804\uCCB4 ' + escapeHtml(subject) + '</span>' +
        '<span class="session-count">' + subjectCount + '\uBB38\uC81C</span></div>';

      tags.forEach(function(tag) {
        var tagCount = filterByTag(tag).filter(function(q) { return q.subject === subject; }).length;
        html += '<div class="session-btn" data-subject="' + escapeHtml(subject) + '" data-tag="' + escapeHtml(tag) + '" role="listitem" tabindex="0">' +
          '<span>' + escapeHtml(tag) + '</span>' +
          '<span class="session-count">' + tagCount + '\uBB38\uC81C</span></div>';
      });

      html += '</div></div>';
    });

    view.innerHTML = html;

    view.querySelectorAll('.year-header').forEach(function(header) {
      header.addEventListener('click', function() {
        var safeId = header.dataset.safeId;
        var panel = view.querySelector('#subj-' + safeId);
        var isOpen = header.classList.toggle('open');
        panel.classList.toggle('open', isOpen);
      });
    });

    view.querySelectorAll('.session-btn').forEach(function(btn) {
      btn.addEventListener('click', function() {
        var subject = btn.dataset.subject;
        var tag = btn.dataset.tag;
        var all = btn.dataset.all;
        if (all) {
          startSession({ type: 'subject', value: subject }, subject);
        } else {
          startSession({ type: 'tag', value: tag, subject: subject }, tag);
        }
      });
    });
  }

  // ================================================================
  // Tag View (Year/Tag/Search)
  // ================================================================

  function renderTagView() {
    var view = $('#view-tag');
    var tagsBySubj = getTagsBySubject();
    var allCounts = countByTag();
    var yearSessions = getYearSessions();
    var yearSessionCounts = countByYearSession();
    var searchTimeout = null;

    view.innerHTML =
      '<div class="section-header"><h2>\uC5F0\uB3C4\uBCC4 / \uD0DC\uADF8\uBCC4</h2></div>' +
      '<div class="search-wrap"><input type="search" class="search-input" id="tag-search"' +
      ' placeholder="\uD0DC\uADF8, \uACFC\uBAA9, \uBB38\uC81C \uAC80\uC0C9..." autocomplete="off"></div>' +
      '<div id="tag-content"></div>';

    var contentEl = view.querySelector('#tag-content');
    var searchInput = view.querySelector('#tag-search');

    function renderTagDefault() {
      var html = '<div class="section-header" style="padding-top:8px"><h2 style="font-size:0.95rem">\uC5F0\uB3C4\uBCC4</h2></div>';

      Object.keys(yearSessions).forEach(function(year) {
        var sessions = yearSessions[year];
        html += '<div class="year-section">' +
          '<div class="year-header" data-year="' + year + '" role="button" tabindex="0">' +
          '<span>' + year + '\uB144</span>' +
          '<span style="font-size:0.8rem;color:var(--muted)">' + sessions.length + '\uD68C\uCC28</span>' +
          '<span class="chevron" aria-hidden="true">\u25BC</span></div>' +
          '<div class="year-sessions" id="year-' + year + '">';

        sessions.forEach(function(session) {
          var cnt = yearSessionCounts[year + '_' + session] || 0;
          html += '<div class="session-btn" data-year="' + year + '" data-session="' + escapeHtml(session) + '" role="button" tabindex="0">' +
            '<span>' + year + '\uB144 ' + escapeHtml(session) + '</span>' +
            '<span class="session-count">' + cnt + '\uBB38\uC81C</span></div>';
        });
        html += '</div></div>';
      });

      html += '<div class="section-header" style="padding-top:12px"><h2 style="font-size:0.95rem">\uD0DC\uADF8\uBCC4</h2></div>';

      Object.keys(tagsBySubj).forEach(function(subject) {
        var tags = tagsBySubj[subject];
        html += '<div class="section-header" style="padding-top:4px;padding-bottom:4px">' +
          '<span style="font-size:0.85rem;color:var(--muted)">' + escapeHtml(subject) + '</span></div>' +
          '<div class="grid-list" style="padding-top:0">' +
          tags.map(function(tag) { return renderTagCard(tag, allCounts[tag] || 0); }).join('') +
          '</div>';
      });

      contentEl.innerHTML = html;

      // Year toggle
      contentEl.querySelectorAll('.year-header').forEach(function(header) {
        header.addEventListener('click', function() {
          var panel = contentEl.querySelector('#year-' + header.dataset.year);
          var isOpen = header.classList.toggle('open');
          panel.classList.toggle('open', isOpen);
        });
      });

      // Year session click
      contentEl.querySelectorAll('.session-btn').forEach(function(btn) {
        btn.addEventListener('click', function() {
          startSession({ type: 'year', value: btn.dataset.year, session: btn.dataset.session },
            btn.dataset.year + '\uB144 ' + btn.dataset.session);
        });
      });

      // Tag card click
      contentEl.querySelectorAll('.grid-card[data-tag]').forEach(function(card) {
        card.addEventListener('click', function() {
          startSession({ type: 'tag', value: card.dataset.tag }, card.dataset.tag);
        });
      });
    }

    function renderSearchResults(query) {
      var results = searchQuestions(query, 60);
      if (results.length === 0) {
        contentEl.innerHTML = '<div class="empty-state">\uAC80\uC0C9 \uACB0\uACFC\uAC00 \uC5C6\uC2B5\uB2C8\uB2E4.<br><small style="font-size:0.8rem">"' + escapeHtml(query) + '"</small></div>';
        return;
      }
      contentEl.innerHTML =
        '<div class="section-header"><span style="font-size:0.9rem;color:var(--muted)">"' + escapeHtml(query) + '" \uAC80\uC0C9 \uACB0\uACFC ' + results.length + '\uAC74</span></div>' +
        '<div class="wrong-list">' +
        results.map(function(q) { return renderQuestionListItem(q, state.progressMap[q._id]); }).join('') +
        '</div>';

      contentEl.querySelectorAll('.wrong-item').forEach(function(item) {
        item.addEventListener('click', function() {
          var idx = 0;
          for (var i = 0; i < results.length; i++) {
            if (results[i]._id === item.dataset.qId) { idx = i; break; }
          }
          startSession({ type: 'search', results: results }, '"' + query + '"', idx);
        });
      });
    }

    searchInput.addEventListener('input', function() {
      clearTimeout(searchTimeout);
      var query = searchInput.value.trim();
      if (!query) { renderTagDefault(); return; }
      searchTimeout = setTimeout(function() { renderSearchResults(query); }, 300);
    });

    renderTagDefault();
  }

  // ================================================================
  // Wrong Answer View
  // ================================================================

  function renderWrongView() {
    var view = $('#view-wrong');

    getWrongIds().then(function(wrongIds) {
      if (wrongIds.length === 0) {
        view.innerHTML =
          '<div class="section-header"><h2>\uC624\uB2F5\uB178\uD2B8</h2></div>' +
          '<div class="empty-state"><span class="empty-icon" aria-hidden="true">\uD83D\uDCDD</span>' +
          '\uC544\uC9C1 \uC624\uB2F5\uC774 \uC5C6\uC2B5\uB2C8\uB2E4.<br>\uBB38\uC81C\uB97C \uD480\uACE0 \uD2C0\uB9B0 \uBB38\uC81C\uAC00<br>\uC5EC\uAE30\uC5D0 \uC30D\uC785\uB2C8\uB2E4.</div>';
        return;
      }

      var wrongQuestions = filterByIds(wrongIds);

      view.innerHTML =
        '<div class="section-header"><h2>\uC624\uB2F5\uB178\uD2B8</h2>' +
        '<span class="counter-badge">' + wrongIds.length + '\uBB38\uC81C</span></div>' +
        '<div style="padding:0 16px 8px">' +
        '<button id="review-wrong-btn" class="settings-btn" style="width:100%;min-height:44px;background:rgba(248,81,73,0.12);color:var(--red);border:1px solid rgba(248,81,73,0.3)">' +
        '\uC624\uB2F5 \uBB38\uC81C \uB2E4\uC2DC \uD480\uAE30 (' + wrongIds.length + '\uBB38\uC81C)</button></div>' +
        '<div class="wrong-list">' +
        wrongQuestions.map(function(q) { return renderQuestionListItem(q, state.progressMap[q._id]); }).join('') +
        '</div>';

      view.querySelector('#review-wrong-btn').addEventListener('click', function() {
        startSession({ type: 'wrong', ids: wrongIds }, '\uC624\uB2F5\uB178\uD2B8');
      });

      view.querySelectorAll('.wrong-item').forEach(function(item) {
        item.addEventListener('click', function() {
          var idx = 0;
          for (var i = 0; i < wrongQuestions.length; i++) {
            if (wrongQuestions[i]._id === item.dataset.qId) { idx = i; break; }
          }
          startSession({ type: 'wrong', ids: wrongIds }, '\uC624\uB2F5\uB178\uD2B8', idx);
        });
      });
    });
  }

  // ================================================================
  // Settings View
  // ================================================================

  function renderSettingsView() {
    var view = $('#view-settings');

    getAllProgress().then(function(allProgress) {
      var answered = allProgress.length;
      var correct = allProgress.filter(function(p) { return p.isCorrect; }).length;
      var wrong = allProgress.filter(function(p) { return p.wrongCount > 0; }).length;
      var totalQ = 0;
      var c = countBySubject();
      Object.keys(c).forEach(function(k) { totalQ += c[k]; });

      view.innerHTML =
        '<div class="section-header"><h2>\uC124\uC815</h2></div>' +
        '<div class="stats-grid">' +
        '<div class="stat-card"><div class="stat-value">' + answered + '</div><div class="stat-label">\uD480\uC774 \uC644\uB8CC</div></div>' +
        '<div class="stat-card"><div class="stat-value" style="color:var(--green)">' + correct + '</div><div class="stat-label">\uC815\uB2F5</div></div>' +
        '<div class="stat-card"><div class="stat-value" style="color:var(--red)">' + wrong + '</div><div class="stat-label">\uC624\uB2F5</div></div>' +
        '</div>' +
        '<div class="settings-section"><div class="settings-label">\uB370\uC774\uD130</div>' +
        '<div class="settings-row" id="export-btn" role="button" tabindex="0"><div class="settings-row-text">' +
        '<div class="settings-row-title">\uD559\uC2B5 \uB370\uC774\uD130 \uB0B4\uBCF4\uB0B4\uAE30</div>' +
        '<div class="settings-row-sub">\uD480\uC774 \uAE30\uB85D \uBC0F \uD544\uAE30 \uB0B4\uC6A9 JSON \uC800\uC7A5</div></div>' +
        '<button class="settings-btn">\uB0B4\uBCF4\uB0B4\uAE30</button></div>' +
        '<div class="settings-row" id="import-btn" role="button" tabindex="0"><div class="settings-row-text">' +
        '<div class="settings-row-title">\uD559\uC2B5 \uB370\uC774\uD130 \uAC00\uC838\uC624\uAE30</div>' +
        '<div class="settings-row-sub">\uC774\uC804\uC5D0 \uB0B4\uBCF4\uB0B8 JSON \uD30C\uC77C \uBD88\uB7EC\uC624\uAE30</div></div>' +
        '<button class="settings-btn">\uAC00\uC838\uC624\uAE30</button></div>' +
        '<input type="file" id="import-file-input" accept=".json" style="display:none">' +
        '</div>' +
        '<div class="settings-section"><div class="settings-label">\uCD08\uAE30\uD654</div>' +
        '<div class="settings-row" id="clear-progress-btn" role="button" tabindex="0"><div class="settings-row-text">' +
        '<div class="settings-row-title">\uD480\uC774 \uAE30\uB85D \uC0AD\uC81C</div>' +
        '<div class="settings-row-sub">\uBAA8\uB4E0 \uD480\uC774 \uAE30\uB85D\uC744 \uC0AD\uC81C\uD569\uB2C8\uB2E4</div></div>' +
        '<button class="settings-btn danger">\uC0AD\uC81C</button></div></div>' +
        '<div class="settings-section"><div class="settings-label">\uC571 \uC815\uBCF4</div>' +
        '<div class="settings-row" style="cursor:default"><div class="settings-row-text">' +
        '<div class="settings-row-title">\uC804\uAE30\uAE30\uC0AC \uD559\uC2B5 PWA</div>' +
        '<div class="settings-row-sub">\uAE30\uCD9C\uBB38\uC81C ' + totalQ.toLocaleString() + '\uBB38\uC81C \u00B7 Apple Pencil \uC9C0\uC6D0</div>' +
        '</div></div></div>';

      // Export
      view.querySelector('#export-btn').addEventListener('click', function() {
        exportData().then(function(data) {
          var blob = new Blob([JSON.stringify(data, null, 2)], { type: 'application/json' });
          var url = URL.createObjectURL(blob);
          var a = document.createElement('a');
          a.href = url;
          a.download = 'ee-study-backup-' + new Date().toISOString().slice(0, 10) + '.json';
          a.click();
          URL.revokeObjectURL(url);
        });
      });

      // Import
      var fileInput = view.querySelector('#import-file-input');
      view.querySelector('#import-btn').addEventListener('click', function() { fileInput.click(); });
      fileInput.addEventListener('change', function() {
        var file = fileInput.files[0];
        if (!file) return;
        file.text().then(function(text) {
          var data = JSON.parse(text);
          if (data.version !== 1) { alert('\uC9C0\uC6D0\uD558\uC9C0 \uC54A\uB294 \uD30C\uC77C \uD615\uC2DD\uC785\uB2C8\uB2E4.'); return; }
          return importData(data).then(function() {
            return getAllProgress();
          }).then(function(allP) {
            state.progressMap = {};
            allP.forEach(function(p) { state.progressMap[p.id] = p; });
            alert('\uB370\uC774\uD130\uB97C \uC131\uACF5\uC801\uC73C\uB85C \uAC00\uC838\uC654\uC2B5\uB2C8\uB2E4.');
            renderSettingsView();
          });
        }).catch(function(e) {
          alert('\uD30C\uC77C\uC744 \uC77D\uB294\uB370 \uC2E4\uD328\uD588\uC2B5\uB2C8\uB2E4: ' + e.message);
        });
      });

      // Clear progress
      view.querySelector('#clear-progress-btn').addEventListener('click', function() {
        if (!confirm('\uBAA8\uB4E0 \uD480\uC774 \uAE30\uB85D\uC744 \uC0AD\uC81C\uD558\uC2DC\uACA0\uC2B5\uB2C8\uAE4C?\n\uC774 \uC791\uC5C5\uC740 \uB418\uB3CC\uB9B4 \uC218 \uC5C6\uC2B5\uB2C8\uB2E4.')) return;
        clearAllProgress().then(function() {
          state.progressMap = {};
          alert('\uD480\uC774 \uAE30\uB85D\uC774 \uC0AD\uC81C\uB418\uC5C8\uC2B5\uB2C8\uB2E4.');
          renderSettingsView();
        });
      });
    });
  }

  // ================================================================
  // Session: Start Question View
  // ================================================================

  function startSession(filter, title, startIndex) {
    startIndex = startIndex || 0;
    var questions = [];

    if (!filter) {
      questions = _questions.slice();
    } else if (filter.type === 'subject') {
      questions = filterBySubject(filter.value);
    } else if (filter.type === 'tag') {
      questions = filterByTag(filter.value);
      if (filter.subject) {
        questions = questions.filter(function(q) { return q.subject === filter.subject; });
      }
    } else if (filter.type === 'year') {
      questions = filterByYearSession(filter.value, filter.session);
    } else if (filter.type === 'wrong') {
      questions = filterByIds(filter.ids);
    } else if (filter.type === 'search') {
      questions = filter.results;
    }

    if (questions.length === 0) {
      alert('\uD574\uB2F9 \uC870\uAC74\uC5D0 \uBB38\uC81C\uAC00 \uC5C6\uC2B5\uB2C8\uB2E4.');
      return;
    }

    state.filterContext = filter;
    state.currentQueue = questions;
    state.currentIndex = Math.max(0, Math.min(startIndex, questions.length - 1));
    state.answered = false;
    state.userAnswer = null;

    showTab('question');
    showQuestion();
  }

  // ================================================================
  // Show Question
  // ================================================================

  function showQuestion() {
    var q = currentQuestion();
    if (!q) return;

    flushSave();

    var progress = state.progressMap[q._id];
    var answered = progress && progress.answeredAt ? true : false;

    state.answered = answered;
    state.userAnswer = answered ? (progress.userAnswer || null) : null;

    var container = $('#question-container');
    container.innerHTML = renderQuestionCard(q, {
      answered: state.answered,
      userAnswer: state.userAnswer,
      progress: progress,
    });

    // Bind choice buttons
    container.querySelectorAll('.choice-btn').forEach(function(btn) {
      btn.addEventListener('click', function() {
        handleChoiceClick(parseInt(btn.dataset.choice));
      });
    });

    // Bind solution toggle
    var toggle = container.querySelector('.solution-toggle');
    if (toggle) {
      toggle.addEventListener('click', function() {
        var body = container.querySelector('.solution-body');
        var isOpen = toggle.classList.toggle('open');
        body.classList.toggle('open', isOpen);
        toggle.setAttribute('aria-expanded', isOpen);
        if (isOpen) renderMath(body);
      });
    }

    renderMath(container);
    updateNavBar();

    // Load annotation
    loadAnnotation(q._id).then(function(strokes) {
      loadStrokes(strokes);
    });

    // Scroll to top
    var scrollArea = $('#app-content');
    if (scrollArea) scrollArea.scrollTop = 0;
  }

  // ================================================================
  // Choice Click Handler
  // ================================================================

  function handleChoiceClick(choiceNum) {
    if (state.answered) return;
    var q = currentQuestion();
    if (!q) return;

    state.answered = true;
    state.userAnswer = choiceNum;

    saveProgress(q._id, {
      isCorrect: choiceNum === q.answer,
      userAnswer: choiceNum,
    }).then(function(progressRecord) {
      state.progressMap[q._id] = progressRecord;

      var container = $('#question-container');
      container.innerHTML = renderQuestionCard(q, {
        answered: true,
        userAnswer: choiceNum,
        progress: progressRecord,
      });

      var toggle = container.querySelector('.solution-toggle');
      if (toggle) {
        toggle.addEventListener('click', function() {
          var body = container.querySelector('.solution-body');
          var isOpen = toggle.classList.toggle('open');
          body.classList.toggle('open', isOpen);
          toggle.setAttribute('aria-expanded', isOpen);
          if (isOpen) renderMath(body);
        });
      }

      renderMath(container);
      updateNavBar();
    });
  }

  // ================================================================
  // Navigation Bar
  // ================================================================

  function updateNavBar() {
    var total = state.currentQueue.length;
    $('#nav-counter').textContent = (state.currentIndex + 1) + ' / ' + total;
    $('#nav-prev').disabled = state.currentIndex === 0;
    $('#nav-next').disabled = state.currentIndex === total - 1;

    var pencilBtn = $('#pencil-btn');
    if (isDrawingMode()) {
      pencilBtn.classList.add('drawing');
    } else {
      pencilBtn.classList.remove('drawing');
    }
  }

  // ================================================================
  // Event Binding
  // ================================================================

  function bindEvents() {
    // Tab buttons
    $$('.tab-btn').forEach(function(btn) {
      btn.addEventListener('click', function() { showTab(btn.dataset.tab); });
    });

    // Nav prev/next
    $('#nav-prev').addEventListener('click', function() {
      if (state.currentIndex > 0) {
        state.currentIndex--;
        state.answered = false;
        state.userAnswer = null;
        showQuestion();
      }
    });

    $('#nav-next').addEventListener('click', function() {
      if (state.currentIndex < state.currentQueue.length - 1) {
        state.currentIndex++;
        state.answered = false;
        state.userAnswer = null;
        showQuestion();
      }
    });

    // Swipe navigation
    var touchStartX = 0;
    var touchStartY = 0;
    var content = $('#app-content');

    content.addEventListener('touchstart', function(e) {
      if (isDrawingMode()) return;
      touchStartX = e.touches[0].clientX;
      touchStartY = e.touches[0].clientY;
    }, { passive: true });

    content.addEventListener('touchend', function(e) {
      if (isDrawingMode()) return;
      if (state.activeTab !== 'question') return;
      var dx = e.changedTouches[0].clientX - touchStartX;
      var dy = e.changedTouches[0].clientY - touchStartY;
      if (Math.abs(dx) > 60 && Math.abs(dx) > Math.abs(dy) * 1.5) {
        if (dx < 0 && state.currentIndex < state.currentQueue.length - 1) {
          $('#nav-next').click();
        } else if (dx > 0 && state.currentIndex > 0) {
          $('#nav-prev').click();
        }
      }
    }, { passive: true });

    // Pencil button
    var pencilBtn = $('#pencil-btn');
    var penToolbar = $('#pen-toolbar');

    pencilBtn.addEventListener('click', function() {
      var newMode = !isDrawingMode();
      setDrawingMode(newMode);
      penToolbar.classList.toggle('visible', newMode);
      pencilBtn.classList.toggle('drawing', newMode);
    });

    // Pen tool buttons
    penToolbar.querySelectorAll('.pen-tool-btn[data-tool]').forEach(function(btn) {
      btn.addEventListener('click', function() {
        var tool = btn.dataset.tool;
        setTool(tool);
        penToolbar.querySelectorAll('.pen-tool-btn[data-tool]').forEach(function(b) {
          b.classList.toggle('active', b.dataset.tool === tool);
        });
      });
    });

    // Set initial active tool
    var blackBtn = penToolbar.querySelector('[data-tool="black"]');
    if (blackBtn) blackBtn.classList.add('active');

    // Clear annotation
    var clearBtn = penToolbar.querySelector('#clear-annotation-btn');
    if (clearBtn) {
      clearBtn.addEventListener('click', function() {
        if (!confirm('\uD604\uC7AC \uBB38\uC81C\uC758 \uD544\uAE30\uB97C \uBAA8\uB450 \uC9C0\uC6B0\uC2DC\uACA0\uC2B5\uB2C8\uAE4C?')) return;
        clearStrokes();
        var q = currentQuestion();
        if (q) saveAnnotation(q._id, []);
      });
    }

    // Close pen toolbar
    var closeBtn = penToolbar.querySelector('#close-pen-btn');
    if (closeBtn) {
      closeBtn.addEventListener('click', function() {
        setDrawingMode(false);
        penToolbar.classList.remove('visible');
        pencilBtn.classList.remove('drawing');
      });
    }

    // Keyboard navigation
    document.addEventListener('keydown', function(e) {
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
  }

  // ================================================================
  // Boot
  // ================================================================

  if (document.readyState === 'loading') {
    document.addEventListener('DOMContentLoaded', init);
  } else {
    init();
  }
})();
