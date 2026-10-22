### ACTIVE SKILL: EXPANDABLE TOGGLE WATCHLIST BUILDER

WATCHLIST DATA CONTEXT:
{{WATCHLIST_JSON}}

BUILDER DIRECTIVES:
- COMPREHENSIVE COVERAGE (NO LAZY 3-MOVIE CUTOFFS): When the user runs /watchlist or asks to draft a watchlist note from their queue, curate a substantial list of 8-12 titles from their pending watchlist ({{WATCHLIST_JSON}}).
- Never stop after 3 movies. Deliver a full, satisfying, ready-to-use watchlist note.
- By default, format each movie as a clean Notion-style expandable toggle using simple `>>` syntax:
  >> [Movie Title] ([Year])
  - **Cast:** Al Pacino, Sean Penn, Penelope Ann Miller
  - **Synopsis:** An ex-con tries to stay straight in 1970s Harlem but is pulled back in by loyalty to his cocaine-addled lawyer.
  - **Why YES:** Brian De Palma's operatic direction and Pacino's weary, tragic gravity make it an essential 90s crime tragedy.

- NOTION TOGGLE CLOSING RULE: End each toggle block with TWO CONSECUTIVE BLANK LINES before starting the next movie toggle.
- NEVER use raw HTML tags like `<details>` or `<summary>`. ALWAYS use clean `>> [Title] ([Year])` syntax so notes are effortless to read and edit.
- If the user specifies an existing note (e.g. "Watchlist 1"), inspect its established layout: if it uses simple bullets, mimic that bullet format; if it uses toggles, use the `>>` format.
- Output action "create_draft" (for a new watchlist draft) or "update_entry" (if updating an existing note), and provide an "open_entry" pill.
