import logging
import re
import sqlite3
from typing import Callable

logger = logging.getLogger(__name__)


def deduplicate_and_format_note_body(
    existing_body: str,
    new_body: str,
    mode: str,
    user_message: str,
    inspected_movie_id: int | None = None,
    inspected_movie_title: str | None = None,
    get_connection: Callable[[], sqlite3.Connection] | None = None,
) -> str:
    """Format note entries (bullets, Notion-style >> toggles, raw text) and deduplicate in-place."""
    lower_msg = (user_message or "").lower()
    wants_raw = any(
        w in lower_msg
        for w in [
            "as it is",
            "raw",
            "verbatim",
            "plain text",
            "no toggle",
            "without toggle",
            "dont format",
            "don't format",
        ]
    )
    wants_toggle = (
        any(
            w in lower_msg
            for w in ["toggle", "collapse", "collpase", "collapsible", "expandable", "spoiler"]
        )
        and not wants_raw
    )

    # 1. Identify target movie title candidates
    candidate_titles: list[str] = []
    if inspected_movie_title and len(inspected_movie_title.strip()) >= 2:
        candidate_titles.append(inspected_movie_title.strip())

    if not candidate_titles and inspected_movie_id and get_connection is not None:
        try:
            with get_connection() as conn:
                row = conn.execute(
                    "SELECT title FROM movies WHERE tmdb_id = ?",
                    (inspected_movie_id,),
                ).fetchone()
                if row and row["title"]:
                    candidate_titles.append(row["title"].strip())
        except Exception as exc:
            logger.debug("Could not resolve movie title from SQLite for Grey: %s", exc)

    raw_new_lines = [l.strip() for l in (new_body or "").splitlines() if l.strip()]
    first_line_clean = ""
    if raw_new_lines:
        first_line = raw_new_lines[0]
        first_line_clean = re.sub(
            r"^(?:<details\b[^>]*>|<summary\b[^>]*>|[•\-*]|\d+\.|\>\>|\-\>|[▸▶])\s*",
            "",
            first_line,
        )
        first_line_clean = re.sub(r"</summary>.*$", "", first_line_clean).strip()
        m = re.match(r"^([^(\n:\-\[<]+)", first_line_clean)
        if m:
            extracted = m.group(1).strip()
            if len(extracted) >= 2 and extracted.lower() not in [
                "the",
                "a",
                "an",
                "movie",
                "film",
                "note",
                "critique",
                "review",
                "here",
                "ok",
            ]:
                if extracted not in candidate_titles:
                    candidate_titles.append(extracted)

    # Expand candidate_titles with normalized forms (without 'The', 'A', 'An', and trailing years/plurals)
    expanded_candidates: list[str] = []
    for cand in candidate_titles:
        if cand not in expanded_candidates:
            expanded_candidates.append(cand)
        norm = re.sub(r"^(?:the|a|an)\s+", "", cand, flags=re.IGNORECASE).strip()
        if norm and norm not in expanded_candidates:
            expanded_candidates.append(norm)
        stem = norm.rstrip("s").strip()
        if stem and len(stem) >= 3 and stem not in expanded_candidates:
            expanded_candidates.append(stem)
    candidate_titles = expanded_candidates

    # 2. Check if existing_body contains any candidate title
    existing_text = (existing_body or "").strip()
    matched_cand = None
    for cand in candidate_titles:
        pattern = rf"\b{re.escape(cand)}\b"
        if re.search(pattern, existing_text, re.IGNORECASE):
            matched_cand = cand
            break

    # If user message explicitly mentions a known title in existing_text, prefer that
    if existing_text:
        for line in existing_text.splitlines():
            stripped = line.strip()
            clean_l = re.sub(r"^(?:[•\-*]|\d+\.|\>\>|\-\>|[▸▶]|#+)\s*", "", stripped)
            m = re.match(r"^([^(\n:\-\[<]+)", clean_l)
            if m:
                t = m.group(1).strip()
                if len(t) >= 3 and re.search(rf"\b{re.escape(t)}\b", user_message, re.IGNORECASE):
                    matched_cand = t
                    if t not in candidate_titles:
                        candidate_titles.insert(0, t)
                    break

    # Extract critique block for matched candidate in existing_body if new_body is sparse
    existing_critique = []
    if matched_cand and existing_text:
        lines = existing_text.splitlines()
        cand_pat = rf"\b{re.escape(matched_cand)}\b"
        recording = False
        for line in lines:
            stripped = line.strip()
            if re.search(cand_pat, stripped, re.IGNORECASE):
                recording = True
                continue
            if recording:
                if (
                    stripped.startswith("•")
                    or stripped.startswith("-")
                    or stripped.startswith("*")
                    or stripped.startswith("#")
                    or stripped.startswith(">>")
                    or stripped.startswith("<details")
                ):
                    recording = False
                elif stripped:
                    existing_critique.append(stripped)

    # Convert any raw HTML <details><summary> tags in existing_text or new_body to clean human-readable >> syntax
    if "<details" in existing_text.lower():
        existing_text = re.sub(
            r"<details[^>]*>\s*<summary[^>]*>(.*?)</summary>\s*(.*?)\s*</details>",
            r">> \1\n\2\n",
            existing_text,
            flags=re.DOTALL | re.IGNORECASE,
        ).strip()

    formatted_entry = (new_body or "").strip()
    if "<details" in formatted_entry.lower():
        formatted_entry = re.sub(
            r"<details[^>]*>\s*<summary[^>]*>(.*?)</summary>\s*(.*?)\s*</details>",
            r">> \1\n\2\n",
            formatted_entry,
            flags=re.DOTALL | re.IGNORECASE,
        ).strip()

    # 3. Format entry / toggle using clean Notion-style >> syntax
    already_has_toggle = (
        formatted_entry.startswith(">>")
        or "\n>>" in f"\n{formatted_entry}"
        or formatted_entry.startswith("->")
        or "\n->" in f"\n{formatted_entry}"
    )

    if wants_toggle and not already_has_toggle:
        summary_title = (
            first_line_clean
            or matched_cand
            or (candidate_titles[0] if candidate_titles else "Notes")
        )
        if raw_new_lines and (
            raw_new_lines[0].startswith("•")
            or raw_new_lines[0].startswith("-")
            or raw_new_lines[0].startswith("*")
        ):
            summary_title = re.sub(r"^[•\-*]\s*", "", raw_new_lines[0]).strip()
            body_content = "\n\n".join(raw_new_lines[1:]).strip()
        elif raw_new_lines and any(
            cand.lower() in raw_new_lines[0].lower() for cand in candidate_titles
        ):
            summary_title = raw_new_lines[0].strip()
            body_content = "\n\n".join(raw_new_lines[1:]).strip()
        else:
            body_content = formatted_entry

        if not body_content and existing_critique:
            body_content = "\n\n".join(existing_critique)

        if not body_content:
            body_content = formatted_entry or "Personal critique"

        formatted_entry = f">> {summary_title}\n{body_content}\n"

    if wants_raw:
        if formatted_entry.startswith(">>") or formatted_entry.startswith("->"):
            fe_lines = formatted_entry.splitlines()
            if len(fe_lines) > 1:
                formatted_entry = "\n".join(fe_lines[1:]).strip()
            else:
                formatted_entry = re.sub(r"^(?:>>|->)\s*", "", formatted_entry).strip()

    if not existing_text:
        return formatted_entry

    if not formatted_entry:
        return existing_text

    if not matched_cand:
        if mode == "append":
            return f"{existing_text}\n\n{formatted_entry}" if formatted_entry else existing_text
        return formatted_entry if formatted_entry else existing_text

    # 4. In-place upsert and deduplication
    lines = existing_text.splitlines()
    cand_pattern = rf"\b{re.escape(matched_cand)}\b"

    target_entry_idx = None
    for idx, line in enumerate(lines):
        stripped = line.strip()
        is_entry_start = (
            stripped.startswith("•")
            or stripped.startswith("-")
            or stripped.startswith("*")
            or stripped.startswith(">>")
            or stripped.startswith("->")
            or stripped.startswith("▶")
            or stripped.startswith("▸")
            or stripped.startswith("#")
            or bool(re.match(r"^\d+\.\s+", stripped))
        )
        if is_entry_start and re.search(cand_pattern, stripped, re.IGNORECASE):
            target_entry_idx = idx
            if (
                wants_toggle
                and formatted_entry.startswith(">> ")
                and (
                    stripped.startswith("•")
                    or stripped.startswith("-")
                    or stripped.startswith("*")
                )
            ):
                rich_summary = re.sub(r"^[•\-*]\s*", "", stripped).strip()
                lines_f = formatted_entry.splitlines()
                body_rest = "\n".join(lines_f[1:])
                formatted_entry = f">> {rich_summary}\n{body_rest}\n"
            break

    if target_entry_idx is not None:
        new_lines = []
        replaced = False
        skip_following_critique = False

        for idx, line in enumerate(lines):
            stripped = line.strip()

            if idx == target_entry_idx:
                new_lines.append(formatted_entry.rstrip())
                new_lines.append("")
                new_lines.append("")
                replaced = True
                skip_following_critique = True
                continue

            if re.search(cand_pattern, stripped, re.IGNORECASE) and replaced:
                skip_following_critique = True
                continue

            if skip_following_critique:
                is_next_item = (
                    stripped.startswith("•")
                    or stripped.startswith("-")
                    or stripped.startswith("*")
                    or stripped.startswith(">>")
                    or stripped.startswith("->")
                    or stripped.startswith("▶")
                    or stripped.startswith("▸")
                    or stripped.startswith("#")
                    or stripped.startswith("<details")
                    or bool(re.match(r"^\d+\.\s+", stripped))
                )
                if is_next_item:
                    skip_following_critique = False
                    new_lines.append(line)
                elif not stripped:
                    continue
                else:
                    continue
            else:
                new_lines.append(line)

        cleaned_result = "\n".join(new_lines)
        cleaned_result = re.sub(r"\n{3,}", "\n\n", cleaned_result).strip()
        return cleaned_result

    if mode == "append":
        return f"{existing_text}\n\n{formatted_entry}" if formatted_entry else existing_text
    return formatted_entry if formatted_entry else existing_text
