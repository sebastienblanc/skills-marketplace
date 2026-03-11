# Contributing a Skill

Thank you for contributing to the SCIAM Skills Marketplace! Follow these steps to add a new skill.

---

## 1. Fork & clone the repository

```bash
git clone https://github.com/sciam/skills-marketplace.git
cd skills-marketplace
```

## 2. Create your skill directory

```bash
mkdir -p skills/<your-skill-name>/references
```

Use **kebab-case** for the directory name (e.g., `react-code-review`, `k8s-debugging`, `sql-optimization`).

## 3. Write your skill

Copy the template and fill it in:

```bash
cp SKILL_TEMPLATE.md skills/<your-skill-name>/SKILL.md
```

### Required frontmatter fields

```yaml
---
name: <skill-name>          # must match the directory name (kebab-case)
description: >              # one or two sentence summary shown on the marketplace card
  <Short description>
license: Apache-2.0         # SPDX identifier
metadata:
  author: <Your name / org>
  tags: <comma-separated list of lowercase tags>
  icon: 🛠️                  # optional — emoji shown on the card
  difficulty: beginner | intermediate | advanced   # optional
---
```

### Body

The body of `SKILL.md` is the actual prompt injected into the AI assistant. Write it in the second person ("You are a ...") and structure it with numbered steps.

## 4. Add references (optional)

Place any curated reference docs in `skills/<your-skill-name>/references/REFERENCE.md`.

## 5. Preview locally (optional)

```bash
python scripts/generate_skills_json.py
# then open docs/index.html in your browser
```

## 6. Open a Pull Request

- Target branch: `main`
- PR title: `feat(skill): add <skill-name>`
- The CI workflow will validate the frontmatter and regenerate `docs/skills.json`
- Once merged, the marketplace is updated automatically via GitHub Pages

---

## Skill Quality Guidelines

| Criterion | Expectation |
|-----------|-------------|
| **Focus** | One clear, specific task per skill |
| **Structure** | Numbered steps with clear headings |
| **Examples** | Include at least one concrete example or reference |
| **Tags** | Minimum 2, maximum 8 lowercase tags |
| **Description** | ≤ 200 characters (fits on the card) |

---

## Code of Conduct

Be respectful. All contributions must be original or properly attributed. Do not include proprietary content.
