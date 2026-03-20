"""Korean text normalization for electrical engineering exam content."""
import re
import unicodedata


# @MX:NOTE: [AUTO] Primary text normalization utility for Korean EE exam ingestion pipeline.
# Handles unicode normalization, whitespace cleanup, and EE unit standardization.
class KoreanTextNormalizer:
    """
    Normalizes Korean electrical engineering exam text.
    Handles: unicode variants, special symbols, formula notation, choice markers.
    """

    # Korean circle numbers for choices: ①②③④
    CIRCLE_MAP = {"①": "1", "②": "2", "③": "3", "④": "4"}

    # Common EE unit normalization — map unicode variants to canonical forms
    UNIT_MAP = {
        "Ω": "Ω",  # normalize unicode omega variants
        "μ": "μ",  # micro
        "Φ": "Φ",  # flux
    }

    def normalize(self, text: str) -> str:
        """Full normalization pipeline."""
        text = self._normalize_unicode(text)
        text = self._normalize_whitespace(text)
        text = self._normalize_units(text)
        return text.strip()

    def _normalize_unicode(self, text: str) -> str:
        """Apply NFC unicode normalization to ensure consistent codepoints."""
        return unicodedata.normalize("NFC", text)

    def _normalize_whitespace(self, text: str) -> str:
        """Collapse multiple spaces/tabs and reduce excessive newlines."""
        text = re.sub(r"[ \t]+", " ", text)
        text = re.sub(r"\n{3,}", "\n\n", text)
        return text

    def _normalize_units(self, text: str) -> str:
        """Replace unicode unit variants with canonical forms."""
        for variant, standard in self.UNIT_MAP.items():
            text = text.replace(variant, standard)
        return text

    def replace_circle_numbers(self, text: str) -> str:
        """Replace Korean circle numbers ①②③④ with plain digits 1234."""
        for circle, digit in self.CIRCLE_MAP.items():
            text = text.replace(circle, digit)
        return text

    def extract_numbers_with_units(self, text: str) -> list[dict]:
        """
        Extract numerical values with units from text.
        Returns list of {"value": float, "unit": str, "original": str}
        """
        pattern = r"([\d.]+)\s*(Ω|V|A|W|kW|kV|MVA|Hz|F|H|mH|μF|kΩ|MΩ)"
        matches = re.finditer(pattern, text)
        results = []
        for m in matches:
            try:
                results.append(
                    {
                        "value": float(m.group(1)),
                        "unit": m.group(2),
                        "original": m.group(0),
                    }
                )
            except ValueError:
                pass
        return results

    def extract_formulas(self, text: str) -> list[str]:
        """Extract formula-like patterns (e.g., V=IR, P=VI, Z=√(R²+X²))."""
        pattern = r"[A-Za-z_]\s*=\s*[^,。\n]{2,30}"
        return re.findall(pattern, text)
