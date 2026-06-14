// Data store: question loading, filtering, searching
// All questions are loaded into memory for fast access

let _questions = [];
let _stats = null;

// Unique question ID
export function qId(q) {
  return `${q.year}_${q.session}_${q.q_no}`;
}

// ===========================
// Data Loading
// ===========================

export async function loadQuestions(onProgress) {
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

export async function loadStats() {
  if (_stats) return _stats;
  try {
    const response = await fetch('./data/stats.json');
    _stats = await response.json();
    return _stats;
  } catch {
    return null;
  }
}

export function getQuestions() {
  return _questions;
}

// ===========================
// Filtering
// ===========================

export function filterBySubject(subject) {
  return _questions.filter((q) => q.subject === subject);
}

export function filterByTag(tag) {
  return _questions.filter((q) => q.tag === tag);
}

export function filterByYearSession(year, session) {
  return _questions.filter(
    (q) => q.year === parseInt(year) && q.session === session
  );
}

export function filterByIds(ids) {
  const idSet = new Set(ids);
  const map = new Map(_questions.map((q) => [q._id, q]));
  return ids.map((id) => map.get(id)).filter(Boolean);
}

// ===========================
// Stats from loaded data
// ===========================

export function getSubjects() {
  const subjectSet = new Set(_questions.map((q) => q.subject).filter(Boolean));
  return Array.from(subjectSet).sort();
}

export function getTagsBySubject() {
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

export function getYearSessions() {
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

export function countBySubject() {
  const counts = {};
  for (const q of _questions) {
    counts[q.subject] = (counts[q.subject] || 0) + 1;
  }
  return counts;
}

export function countByTag() {
  const counts = {};
  for (const q of _questions) {
    if (q.tag) counts[q.tag] = (counts[q.tag] || 0) + 1;
  }
  return counts;
}

export function countByYearSession() {
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

export function search(query, limit = 50) {
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
