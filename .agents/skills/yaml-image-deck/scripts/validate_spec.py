#!/usr/bin/env python3
import argparse
from pathlib import Path
import sys

try:
    import yaml
except ImportError:
    raise SystemExit("PyYAML is required: python -m pip install PyYAML")


ALLOWED_LAYOUTS = {
    "cover_hero", "question_focus", "misconception_dual", "comparison_split",
    "process_timeline", "classification_grid", "case_scene_analysis",
    "relationship_map", "data_focus", "summary_three", "action_next_step",
    "section_divider",
}


def require(mapping, key, where, errors):
    if not isinstance(mapping, dict) or key not in mapping:
        errors.append(f"{where}: missing {key}")


def main():
    parser = argparse.ArgumentParser()
    parser.add_argument("--spec", required=True)
    args = parser.parse_args()
    path = Path(args.spec)
    data = yaml.safe_load(path.read_text(encoding="utf-8"))
    errors = []

    for key in ("schema_version", "deck", "canvas", "design_system", "layout_router", "slides", "validation"):
        require(data, key, "root", errors)

    slides = data.get("slides", []) if isinstance(data, dict) else []
    if not isinstance(slides, list) or not slides:
        errors.append("root: slides must be a non-empty list")
        slides = []

    pages = []
    for index, slide in enumerate(slides, 1):
        where = f"slides[{index}]"
        for key in ("page", "role", "core_point", "semantic_structure", "layout", "visible_text", "visual", "output"):
            require(slide, key, where, errors)
        if isinstance(slide, dict):
            pages.append(slide.get("page"))
            layout_id = (slide.get("layout") or {}).get("id") if isinstance(slide.get("layout"), dict) else None
            if layout_id and layout_id not in ALLOWED_LAYOUTS:
                errors.append(f"{where}: unsupported layout id {layout_id}")

    if len(pages) != len(set(pages)):
        errors.append("slides: duplicate page numbers")
    if pages and pages != list(range(1, len(pages) + 1)):
        errors.append("slides: page numbers must be sequential from 1")

    expected = (data.get("deck") or {}).get("slide_count") if isinstance(data, dict) else None
    if expected is not None and expected != len(slides):
        errors.append(f"deck.slide_count={expected}, but slides has {len(slides)} entries")

    font_feel = (((data.get("design_system") or {}).get("typography") or {}).get("font_feel", ""))
    if not any(token in str(font_feel).lower() for token in ("圓", "round")):
        errors.append("design_system.typography.font_feel must require rounded typography")

    if errors:
        print("INVALID")
        for error in errors:
            print(f"- {error}")
        return 1
    print(f"VALID: {path} ({len(slides)} slides)")
    return 0


if __name__ == "__main__":
    sys.exit(main())

