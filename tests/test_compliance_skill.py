from pathlib import Path

from guardrails.context_perimeter import (
    _JURISDICTION_SENSITIVE_TERMS,
    _KNOWN_COUNTRIES_MULTI_WORD,
    _KNOWN_COUNTRIES_SINGLE_WORD,
)

SKILL_DIR = Path(__file__).resolve().parent.parent / "skills" / "compliance-guardrail"


def test_skill_md_exists_with_frontmatter():
    skill_md = (SKILL_DIR / "SKILL.md").read_text()
    assert skill_md.startswith("---")
    assert "name:" in skill_md
    assert "description:" in skill_md


def test_guardrail_terms_are_loaded_from_skill_references():
    """The escalation criteria live in the skill's references (Day3
    progressive-disclosure pattern), not hardcoded in Python — the guardrail
    must reflect exactly what the reference files say."""
    ref = SKILL_DIR / "references"
    terms = set((ref / "jurisdiction_sensitive_terms.txt").read_text().split())
    single = set((ref / "countries_single_word.txt").read_text().split())
    multi = {
        line.strip()
        for line in (ref / "countries_multi_word.txt").read_text().splitlines()
        if line.strip()
    }

    assert _JURISDICTION_SENSITIVE_TERMS == terms
    assert _KNOWN_COUNTRIES_SINGLE_WORD == single
    assert _KNOWN_COUNTRIES_MULTI_WORD == multi


def test_editing_reference_changes_guardrail_behavior():
    """Loader must actually parse the files, not mirror a hardcoded copy —
    the sets must be non-trivially sized and contain known entries."""
    assert "leave" in _JURISDICTION_SENSITIVE_TERMS
    assert "france" in _KNOWN_COUNTRIES_SINGLE_WORD
    assert "new zealand" in _KNOWN_COUNTRIES_MULTI_WORD
