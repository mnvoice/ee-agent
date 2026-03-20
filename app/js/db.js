// IndexedDB wrapper for annotations and study progress
// Stores: annotations, progress, questions_cache

const DB_NAME = 'ee-study-db';
const DB_VERSION = 2;

let _db = null;

export function openDB() {
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

export async function saveAnnotation(qId, strokes) {
  const store = tx('annotations', 'readwrite');
  await promisify(store.put({ id: qId, strokes, updatedAt: Date.now() }));
}

export async function loadAnnotation(qId) {
  const store = tx('annotations', 'readonly');
  const result = await promisify(store.get(qId));
  return result ? result.strokes : [];
}

export async function deleteAnnotation(qId) {
  const store = tx('annotations', 'readwrite');
  await promisify(store.delete(qId));
}

export async function getAllAnnotations() {
  const store = tx('annotations', 'readonly');
  return promisify(store.getAll());
}

// ===========================
// Progress
// ===========================

// Progress record: { id, answeredAt, isCorrect, userAnswer, wrongCount }

export async function saveProgress(qId, { isCorrect, userAnswer }) {
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

export async function loadProgress(qId) {
  const store = tx('progress', 'readonly');
  return promisify(store.get(qId));
}

export async function getAllProgress() {
  const store = tx('progress', 'readonly');
  return promisify(store.getAll());
}

export async function getWrongIds() {
  const all = await getAllProgress();
  return all
    .filter((p) => p.wrongCount > 0)
    .sort((a, b) => b.wrongCount - a.wrongCount)
    .map((p) => p.id);
}

export async function clearAllProgress() {
  const store = tx('progress', 'readwrite');
  return promisify(store.clear());
}

// ===========================
// Questions Cache
// ===========================

export async function cacheQuestions(questions) {
  const store = tx('questions_cache', 'readwrite');
  await promisify(store.put({ key: 'all', data: questions, cachedAt: Date.now() }));
}

export async function getCachedQuestions() {
  const store = tx('questions_cache', 'readonly');
  const record = await promisify(store.get('all'));
  return record ? record.data : null;
}

// ===========================
// Export / Import
// ===========================

export async function exportData() {
  const [annotations, progress] = await Promise.all([
    getAllAnnotations(),
    getAllProgress(),
  ]);
  return { annotations, progress, exportedAt: new Date().toISOString(), version: 1 };
}

export async function importData({ annotations = [], progress = [] }) {
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
