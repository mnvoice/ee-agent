"""Korean text embedder using sentence-transformers."""
import logging

import numpy as np

logger = logging.getLogger(__name__)

try:
    from sentence_transformers import SentenceTransformer

    SENTENCE_TRANSFORMERS_AVAILABLE = True
except ImportError:
    SENTENCE_TRANSFORMERS_AVAILABLE = False


class KoreanEmbedder:
    """
    Korean text embedder using snunlp/KR-ELECTRA-discriminator.
    Falls back to deterministic hashing when model unavailable.
    Embedding dimension: 768.
    """

    MODEL_NAME = "snunlp/KR-ELECTRA-discriminator"
    FALLBACK_DIM = 768

    def __init__(self, model_name: str | None = None):
        self._model_name = model_name or self.MODEL_NAME
        self._model = None
        self._initialized = False

    def _lazy_init(self) -> None:
        if self._initialized:
            return
        if SENTENCE_TRANSFORMERS_AVAILABLE:
            try:
                self._model = SentenceTransformer(self._model_name)
                logger.info(f"Loaded embedding model: {self._model_name}")
            except Exception as e:
                logger.warning(f"Failed to load {self._model_name}: {e}. Using fallback.")
        self._initialized = True

    def embed(self, text: str) -> np.ndarray:
        """Embed a single text. Returns float32 array of shape (768,)."""
        self._lazy_init()
        if self._model is not None:
            return self._model.encode(text, normalize_embeddings=True)
        return self._fallback_embed(text)

    def embed_batch(self, texts: list[str]) -> np.ndarray:
        """Embed multiple texts. Returns float32 array of shape (n, 768)."""
        self._lazy_init()
        if self._model is not None:
            return self._model.encode(texts, normalize_embeddings=True)
        return np.array([self._fallback_embed(t) for t in texts])

    def _fallback_embed(self, text: str) -> np.ndarray:
        """
        Deterministic fallback embedding using character hashing.
        NOT semantically meaningful — only for offline testing.
        """
        rng = np.random.RandomState(abs(hash(text)) % (2**31))
        vec = rng.randn(self.FALLBACK_DIM).astype(np.float32)
        norm = np.linalg.norm(vec)
        return vec / norm if norm > 0 else vec

    @property
    def dim(self) -> int:
        return self.FALLBACK_DIM
