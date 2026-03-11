# SCIAM Skills Marketplace

A curated collection of AI Copilot skills, openly published and ready to use.

> **Live Marketplace → [https://sciam.github.io/skills-marketplace](https://sciam.github.io/skills-marketplace)**

---

## What is a Skill?

A **Skill** is a structured prompt file (`SKILL.md`) that turns an AI assistant into a specialized expert for a specific task (migration, code review, architecture design, etc.).

Each skill lives in its own directory under `skills/` and follows a standard format so it can be:

- Discovered and previewed in the marketplace UI
- Copied directly into your AI assistant context
- Versioned, reviewed, and improved via Pull Requests

---

## Repository Structure

```
skills-marketplace/
├── skills/
│   └── <skill-name>/
│       ├── SKILL.md          ← main skill file (required)
│       ├── assets/           ← diagrams, screenshots (optional)
│       └── references/
│           └── REFERENCE.md  ← curated reference material (optional)
├── docs/                     ← GitHub Pages marketplace (auto-generated)
│   ├── index.html
│   └── skills.json
├── scripts/
│   └── generate_skills_json.py
├── SKILL_TEMPLATE.md
└── CONTRIBUTING.md
```

---

## Available Skills

| Skill | Description | Tags |
|-------|-------------|------|
| [spring2quarkus](skills/spring2quarkus/SKILL.md) | Migrate Spring Boot apps to Quarkus from scratch | java, spring-boot, quarkus, migration |

---

## Adding a New Skill

See [CONTRIBUTING.md](CONTRIBUTING.md) for the full process.

**TL;DR:**

1. Copy `SKILL_TEMPLATE.md` into `skills/<your-skill-name>/SKILL.md`
2. Fill in the frontmatter and skill body
3. Open a Pull Request — the marketplace updates automatically on merge

---

## License

All skills are published under their individual licenses (specified in each `SKILL.md` frontmatter). The marketplace UI is [MIT](LICENSE).
