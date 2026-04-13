"""Korean electrical engineer exam question parser."""
import re
import logging
from typing import Optional

from ee_agent.domain.models.question import (
    Choice,
    DifficultyLevel,
    Question,
    QuestionType,
    Subject,
)
from ee_agent.ingestion.normalizer import KoreanTextNormalizer

logger = logging.getLogger(__name__)

# KoNLPy is optional — fall back to regex-based extraction when unavailable.
try:
    from konlpy.tag import Komoran  # type: ignore[import]

    KONLPY_AVAILABLE = True
except (ImportError, Exception):
    KONLPY_AVAILABLE = False


# @MX:ANCHOR: [AUTO] Core entry point for Korean exam text parsing.
# @MX:REASON: Called by ingestion pipeline and tests; fan_in >= 3.
class KoreanQuestionParser:
    """
    Parses Korean electrical engineer exam questions from raw text.
    Uses regex as primary strategy + KoNLPy Komoran for NLP when available.
    """

    # Pattern to match question blocks: "1. stem text ①choice1 ②choice2 ③choice3 ④choice4"
    QUESTION_START = re.compile(r"^(\d{1,3})[.．]\s*", re.MULTILINE)
    CHOICE_PATTERN = re.compile(r"[①②③④]\s*([^\n①②③④]{1,200})")

    # Hollow and filled circle markers; filled (❶❷❸❹) indicate correct answer
    _HOLLOW = "①②③④"
    _FILLED = "❶❷❸❹"
    _ALL_CIRCLES = _HOLLOW + _FILLED

    # Subject detection keyword mapping
    SUBJECT_KEYWORDS: dict[Subject, list[str]] = {
        Subject.ELECTROMAGNETISM: [
            "자기장", "자계", "자속", "투자율", "유전율", "전계", "전기력선",
            "쿨롱", "패러데이", "렌츠", "앙페르", "맥스웰", "전자기",
            "자성", "자화", "자기유도", "전자유도", "자기력", "전위",
            "가우스", "정전용량", "전기쌍극자", "벡터", "스칼라",
        ],
        Subject.ELECTRICAL_MACHINES: [
            "변압기", "전동기", "발전기", "유도기", "동기기", "정류기",
            "유도전동기", "동기발전기", "직류기", "권선", "슬립",
            "회전수", "토크", "효율", "전기자", "계자", "정류자",
        ],
        Subject.POWER_SYSTEMS: [
            "송전", "배전", "계통", "차단기", "선로", "전력조류",
            "코로나", "애자", "철탑", "가공", "지중", "변전소",
            "전압강하", "전력손실", "역률개선", "보호계전", "안정도",
            "방사상", "환상선로", "과전류계전기", "OCR", "DOCR",
            "방향성", "단락보호", "지락보호", "계전기", "전력계통",
        ],
        Subject.CIRCUIT_THEORY: [
            "라플라스", "전달함수", "4단자", "분포정수", "과도현상",
            "비정현파", "푸리에", "대칭좌표", "영상분", "정상분", "역상분",
            "임피던스매칭", "어드미턴스", "공진주파수", "Q인수",
        ],
        Subject.CONTROL_ENGINEERING: [
            "제어", "피드백", "안정도", "보드선도", "나이퀴스트",
            "PID", "전달함수", "블록선도", "상태방정식", "근궤적",
            "시정수", "감쇠", "Z변환", "샘플링", "디지털제어",
        ],
        Subject.ELECTRICAL_SAFETY: [
            "기술기준", "KEC", "규정", "조항", "시설기준",
            "접지", "절연", "보호등급", "이격거리", "허용전류",
            "누전차단기", "배선", "전선관", "가공전선", "지중전선",
        ],
    }

    # EE technical terms for concept extraction (used when KoNLPy is unavailable)
    EE_TERMS = [
        "옴의 법칙",
        "키르히호프",
        "패러데이",
        "렌츠",
        "쿨롱",
        "변압기",
        "전동기",
        "발전기",
        "인버터",
        "정류기",
        "임피던스",
        "리액턴스",
        "커패시턴스",
        "인덕턴스",
        "유효전력",
        "무효전력",
        "피상전력",
        "역률",
        "중성점",
        "3상",
        "단상",
        "영상분",
        "정상분",
        "역상분",
        "차단기",
        "보호계전기",
        "영상변류기",
        "라플라스",
        "전달함수",
        "보드선도",
        "나이퀴스트",
    ]

    def __init__(self) -> None:
        self._normalizer = KoreanTextNormalizer()
        self._komoran: Optional[object] = None
        if KONLPY_AVAILABLE:
            try:
                self._komoran = Komoran()  # type: ignore[name-defined]
            except Exception as exc:  # pragma: no cover
                logger.warning("Komoran initialization failed: %s", exc)

    # ------------------------------------------------------------------
    # Public API
    # ------------------------------------------------------------------

    def parse_text(
        self,
        raw_text: str,
        year: int = 2023,
        session: int = 1,
        page_offsets: Optional[list[int]] = None,
    ) -> list[Question]:
        """
        Parse multiple questions from raw exam text.

        Splits on question-number boundaries and delegates each block to
        parse_question_block.  Returns only successfully parsed questions.

        Note: circle-number markers (①②③④) are preserved here so that
        _extract_choices can detect them reliably inside each block.
        """
        # Normalization can shift character offsets; we normalize first, then
        # locate each question on the normalized string. Page offsets are
        # derived from the pre-normalized text, so they remain approximate but
        # sufficient for page-level mapping.
        raw_text = self._normalizer.normalize(raw_text)

        # Split text into blocks at each question-number boundary
        splits = list(self.QUESTION_START.finditer(raw_text))
        if not splits:
            return []

        def position_to_page(pos: int) -> Optional[int]:
            if not page_offsets:
                return None
            # Find largest offset <= pos; 1-indexed page number.
            page = 0
            for idx, off in enumerate(page_offsets):
                if off <= pos:
                    page = idx + 1
                else:
                    break
            return page or 1

        questions: list[Question] = []
        seen_numbers: set[int] = set()
        for i, match in enumerate(splits):
            start = match.start()
            end = splits[i + 1].start() if i + 1 < len(splits) else len(raw_text)
            block = raw_text[start:end].strip()
            q_num = int(match.group(1))
            # Filter: valid range 1~100, skip duplicates
            if q_num < 1 or q_num > 100:
                logger.debug("Skipping out-of-range question number %d", q_num)
                continue
            if q_num in seen_numbers:
                logger.debug("Skipping duplicate question number %d", q_num)
                continue
            source_page = position_to_page(start)
            question = self.parse_question_block(
                block, year, session, q_num, source_page=source_page
            )
            if question is not None:
                seen_numbers.add(q_num)
                questions.append(question)

        return questions

    def parse_question_block(
        self,
        block: str,
        year: int,
        session: int,
        q_num: int,
        source_page: Optional[int] = None,
    ) -> Optional[Question]:
        """
        Parse a single question block into a Question domain object.

        Returns None when the block does not contain enough information
        (e.g. no choices found).
        """
        try:
            # Strip leading question number prefix
            block = self.QUESTION_START.sub("", block, count=1).strip()

            choices, correct_answer, needs_ocr = self._extract_choices(block)
            if not choices:
                logger.debug("No choices found for question %d — skipping", q_num)
                return None

            # Remove choice text from stem
            first_choice_pos = self._find_first_choice_pos(block)
            stem = block[:first_choice_pos].strip() if first_choice_pos > 0 else block

            subject = self._detect_subject(stem)
            q_type = self._detect_question_type(stem)
            difficulty = self._guess_difficulty(stem, choices)

            return Question(
                year=year,
                exam_session=session,
                question_number=q_num,
                subject=subject,
                question_type=q_type,
                difficulty=difficulty,
                stem=stem,
                choices=choices,
                correct_answer=correct_answer,
                tags=self.extract_technical_terms(stem),
                needs_ocr=needs_ocr,
                source_page=source_page,
            )
        except Exception as exc:
            logger.warning("Failed to parse question block %d: %s", q_num, exc)
            return None

    # ------------------------------------------------------------------
    # Internal helpers
    # ------------------------------------------------------------------

    # Page-header noise patterns that appear between choice markers in CBT PDFs.
    _NOISE_PATTERNS = [
        re.compile(r"증\s*기출문제[^\n]*"),
        re.compile(r"전자문제집\s*CBT\s*:\s*www\.comcbt\.com[^\n]*"),
        re.compile(r"전기기사\s*[◐◑][^\n]*"),
        re.compile(r"최강\s*자\s*[◐◑]?[^\n]*"),
    ]

    # Placeholder text injected when a choice marker has no extractable body.
    _OCR_PLACEHOLDER = "[formula - OCR required]"

    def _strip_noise(self, text: str) -> str:
        """Remove PDF page-header artifacts that appear between choice markers."""
        cleaned = text
        for pattern in self._NOISE_PATTERNS:
            cleaned = pattern.sub("", cleaned)
        return cleaned

    # @MX:ANCHOR: [AUTO] Position-based choice extraction; splits on marker positions
    # so empty/formula-only choices can still be preserved for Vision OCR follow-up.
    # @MX:REASON: Previous regex {1,200} rejected empty content, causing ~18 per PDF
    # to be silently skipped despite having valid markers and correct-answer info.
    def _extract_choices(self, text: str) -> tuple[list[Choice], int, bool]:
        """
        Extract four answer choices and the correct answer index.

        Splits the text on circle-marker positions so that even empty/
        formula-only choices are preserved. Missing positions are padded with
        an OCR placeholder.

        Returns:
            (choices, correct_answer_index, needs_ocr) where index is 1-based
            and needs_ocr indicates at least one choice requires Vision OCR.
        """
        # Locate every circle marker (hollow or filled) and record its position.
        marker_re = re.compile(r"[①②③④❶❷❸❹]")
        found: list[tuple[int, str]] = [
            (m.start(), m.group()) for m in marker_re.finditer(text)
        ]

        if found:
            # Build (position 1-4, content, is_correct) tuples by slicing text
            # between consecutive marker positions.
            seen: set[int] = set()
            ordered: list[tuple[int, str, bool]] = []
            for idx, (start, marker) in enumerate(found):
                if marker in self._HOLLOW:
                    pos = self._HOLLOW.index(marker) + 1
                    is_correct = False
                else:
                    pos = self._FILLED.index(marker) + 1
                    is_correct = True
                if pos in seen:
                    continue

                content_start = start + len(marker)
                content_end = (
                    found[idx + 1][0] if idx + 1 < len(found) else len(text)
                )
                # Cap at 300 chars to avoid runaway capture when markers are missing.
                content_end = min(content_end, content_start + 300)
                raw = text[content_start:content_end]
                cleaned = self._strip_noise(raw).strip()

                seen.add(pos)
                ordered.append((pos, cleaned, is_correct))

            if ordered:
                ordered.sort(key=lambda x: x[0])
                by_pos = {pos: (txt, ic) for pos, txt, ic in ordered}
                correct = next(
                    (pos for pos, (_, ic) in by_pos.items() if ic), 1
                )

                needs_ocr = False
                choices: list[Choice] = []
                for pos in range(1, 5):
                    if pos in by_pos and by_pos[pos][0]:
                        choices.append(Choice(index=pos, text=by_pos[pos][0]))
                    else:
                        needs_ocr = True
                        choices.append(
                            Choice(index=pos, text=self._OCR_PLACEHOLDER)
                        )
                return choices, correct, needs_ocr

        # Fallback: digit-style markers (1. 2. 3. 4.)
        digit_matches = re.findall(
            r"(?:^|\n)\s*([1-4])[.)\s]\s*([^\n]{1,200})", text
        )
        if digit_matches:
            choices = [
                Choice(index=int(idx), text=content.strip())
                for idx, content in digit_matches[:4]
            ]
            return choices, 1, False

        return [], 1, False

    def _find_first_choice_pos(self, text: str) -> int:
        """Return the character position where the first choice marker appears."""
        for marker in ["①", "②", "③", "④", "❶", "❷", "❸", "❹"]:
            pos = text.find(marker)
            if pos >= 0:
                return pos

        # After circle-number replacement, look for leading digit markers
        match = re.search(r"(?:^|\n)\s*[1-4][.)]\s", text)
        if match:
            return match.start()

        return len(text)

    def _detect_subject(self, text: str) -> Subject:
        """
        Detect the exam subject using keyword matching.

        Returns the subject whose keyword list has the most matches.
        Falls back to ELECTROMAGNETISM when no keywords are found.
        """
        result = self.detect_subject_by_keyword(text)
        return result if result is not None else Subject.ELECTROMAGNETISM

    # @MX:NOTE: [AUTO] Public variant that returns None instead of defaulting to
    # ELECTROMAGNETISM, so callers can decide their own fallback strategy
    # (e.g., number-range mapping for calc-only questions with few keywords).
    def detect_subject_by_keyword(self, text: str) -> Optional[Subject]:
        """Return the highest-scoring subject by keyword, or None if no match."""
        scores: dict[Subject, int] = {s: 0 for s in Subject}
        for subject, keywords in self.SUBJECT_KEYWORDS.items():
            for kw in keywords:
                if kw in text:
                    scores[subject] += 1
        best = max(scores, key=lambda s: scores[s])
        return best if scores[best] > 0 else None

    def _detect_question_type(self, text: str) -> QuestionType:
        """
        Classify question type based on lexical cues.

        Priority: REGULATION > DIAGRAM_ANALYSIS > CALCULATION > MULTIPLE_CHOICE
        """
        # Use multi-character cues to avoid false matches on common Korean syllables
        regulation_cues = ["기술기준", "규정", "조항", "KEC", "법규", "시설기준", "안전율", "접지저항"]
        calc_cues = ["계산", "구하", "몇", "얼마", "값", "=", "공식", "수식"]
        diagram_cues = ["회로", "그림", "도면", "파형", "벡터", "다이어그램"]

        for cue in regulation_cues:
            if cue in text:
                return QuestionType.REGULATION

        for cue in diagram_cues:
            if cue in text:
                return QuestionType.DIAGRAM_ANALYSIS

        for cue in calc_cues:
            if cue in text:
                return QuestionType.CALCULATION

        return QuestionType.MULTIPLE_CHOICE

    def extract_technical_terms(self, text: str) -> list[str]:
        """
        Extract EE technical terms found in text.

        Uses KoNLPy Komoran noun extraction when available;
        otherwise falls back to simple substring matching against EE_TERMS.
        """
        if self._komoran is not None:
            try:
                nouns: list[str] = self._komoran.nouns(text)  # type: ignore[attr-defined]
                ee_set = {t for term in self.EE_TERMS for t in [term]}
                return [n for n in nouns if n in ee_set]
            except Exception as exc:  # pragma: no cover
                logger.debug("Komoran extraction failed: %s", exc)

        # Regex fallback — match multi-character EE terms by substring
        found: list[str] = []
        for term in self.EE_TERMS:
            if term in text and term not in found:
                found.append(term)
        return found

    def _guess_difficulty(self, text: str, choices: list[Choice]) -> DifficultyLevel:
        """
        Heuristic difficulty estimation.

        Hard signals: complex formulas, many technical terms, long stem.
        Easy signals: short stem, basic vocabulary.
        Everything else is Medium.
        """
        hard_cues = ["√", "∫", "라플라스", "대칭분", "영상분", "역상분", "복소수", "미분방정식"]
        easy_cues = ["옴의 법칙", "기본", "단순", "간단"]

        for cue in hard_cues:
            if cue in text:
                return DifficultyLevel.HARD

        # Long stem with many technical terms → hard
        technical_count = len(self.extract_technical_terms(text))
        if len(text) > 200 and technical_count >= 3:
            return DifficultyLevel.HARD

        for cue in easy_cues:
            if cue in text:
                return DifficultyLevel.EASY

        # Short stem with few terms → easy
        if len(text) < 80 and technical_count <= 1:
            return DifficultyLevel.EASY

        return DifficultyLevel.MEDIUM
