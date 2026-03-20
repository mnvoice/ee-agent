"""PDF extraction for Korean electrical engineer exam PDFs."""
import logging
import re
from dataclasses import dataclass, field
from pathlib import Path
from typing import Generator

logger = logging.getLogger(__name__)

# pdfplumber is optional — extraction is disabled gracefully when unavailable.
try:
    import pdfplumber  # type: ignore[import]

    PDFPLUMBER_AVAILABLE = True
except ImportError:
    PDFPLUMBER_AVAILABLE = False


@dataclass
class ExtractedPage:
    """Container for text and image metadata extracted from a single PDF page."""

    page_number: int
    text: str
    has_images: bool
    image_bboxes: list[tuple] = field(default_factory=list)


# @MX:NOTE: [AUTO] PDF text extraction layer; returns empty results when pdfplumber absent.
class PDFExtractor:
    """
    Extracts text and image metadata from Korean exam PDFs using pdfplumber.
    Handles multi-column layouts common in Korean exam papers.
    """

    def __init__(self) -> None:
        if not PDFPLUMBER_AVAILABLE:
            logger.warning("pdfplumber not available. PDF extraction disabled.")

    def extract_pages(self, pdf_path: str | Path) -> list[ExtractedPage]:
        """
        Extract all pages from PDF.

        Returns an empty list when pdfplumber is unavailable so that callers
        can degrade gracefully without raising ImportError.

        Raises:
            FileNotFoundError: When the PDF path does not exist.
        """
        if not PDFPLUMBER_AVAILABLE:
            return []

        pdf_path = Path(pdf_path)
        if not pdf_path.exists():
            raise FileNotFoundError(f"PDF not found: {pdf_path}")

        pages: list[ExtractedPage] = []
        with pdfplumber.open(pdf_path) as pdf:
            for i, page in enumerate(pdf.pages, 1):
                text = self._extract_two_column_text(page)
                images = page.images or []
                pages.append(
                    ExtractedPage(
                        page_number=i,
                        text=text,
                        has_images=len(images) > 0,
                        image_bboxes=[
                            (img["x0"], img["y0"], img["x1"], img["y1"]) for img in images
                        ],
                    )
                )

        return pages

    @staticmethod
    def _extract_two_column_text(page) -> str:
        """Extract text from a 2-column page by separating left and right columns."""
        mid_x = page.width / 2
        left_bbox = (0, 0, mid_x, page.height)
        right_bbox = (mid_x, 0, page.width, page.height)
        left_text = page.within_bbox(left_bbox).extract_text() or ""
        right_text = page.within_bbox(right_bbox).extract_text() or ""
        return left_text + "\n" + right_text

    def extract_full_text(self, pdf_path: str | Path) -> str:
        """Extract all text concatenated from PDF, separated by newlines."""
        pages = self.extract_pages(pdf_path)
        return "\n".join(p.text for p in pages)

    def extract_question_sections(self, pdf_path: str | Path) -> Generator[str, None, None]:
        """
        Yield text sections likely containing individual questions.

        Splits on question-number patterns so each yielded string starts
        with a question number prefix (e.g. "1. ", "12. ").
        """
        full_text = self.extract_full_text(pdf_path)
        sections = re.split(r"(?=\n\d{1,3}[.．]\s)", full_text)
        for section in sections:
            stripped = section.strip()
            if stripped:
                yield stripped
