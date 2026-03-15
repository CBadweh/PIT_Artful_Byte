---
name: commit-conventions
description: All commits in this repo must follow Conventional Commits format with a body explaining WHY, per Lesson 8 best practices.
type: feedback
---

All commits must follow Conventional Commits format:

```
type(scope): short description (max 50 chars, imperative mood)

Body: explain WHY this change is needed.

Footer: Lesson X, related context
```

Types: `feat`, `fix`, `build`, `docs`, `refactor`, `test`, `style`

Each commit must:
1. Contain only one logical change (don't bundle unrelated changes)
2. Build successfully
3. Have a body paragraph explaining WHY, not just what

**Why:** Lesson 8 review (2026-03-14) found zero recent commits following this format. Commit messages were vague one-liners like "added lession 6 7 note" with no body text.

**How to apply:** When the user asks to commit, draft the message in Conventional Commits format with a WHY body. If the user provides a vague message, suggest a properly formatted alternative before committing.
