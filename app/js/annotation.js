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

export function initAnnotation(canvas, onSave) {
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

export function resizeCanvas() {
  if (!_canvas) return;
  const rect = _canvas.getBoundingClientRect();
  _canvas.width = rect.width;
  _canvas.height = rect.height;
  redrawAll();
}

// ===========================
// Drawing Mode
// ===========================

export function setDrawingMode(enabled) {
  _isDrawingMode = enabled;
  if (enabled) {
    _canvas.classList.add('drawing-mode');
  } else {
    _canvas.classList.remove('drawing-mode');
  }
}

export function isDrawingMode() {
  return _isDrawingMode;
}

// ===========================
// Tool Selection
// ===========================

export function setTool(toolName) {
  if (TOOLS[toolName] !== undefined || toolName === 'eraser') {
    _currentTool = toolName;
  }
}

export function getCurrentTool() {
  return _currentTool;
}

// ===========================
// Stroke Management
// ===========================

export function loadStrokes(strokes) {
  _strokes = strokes ? JSON.parse(JSON.stringify(strokes)) : [];
  _dirty = false;
  redrawAll();
}

export function clearStrokes() {
  _strokes = [];
  _dirty = true;
  redrawAll();
  scheduleSave();
}

export function getStrokes() {
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
export function flushSave() {
  if (_saveTimer) {
    clearTimeout(_saveTimer);
    _saveTimer = null;
  }
  if (_dirty && _onSave) {
    _onSave(_strokes);
    _dirty = false;
  }
}
