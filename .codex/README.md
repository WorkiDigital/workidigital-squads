# Worki custom agents for Codex

The TOML files in `agents/` are project-scoped generated artifacts. They embed the reviewed upstream specialist instructions, the matching Worki skill, and the repository safety contract.

Regenerate and verify:

```bash
python3 scripts/generate_codex_agents.py
python3 scripts/generate_codex_agents.py --check
```

The source roster is `worki/codex-agents.json`; stage sources are in `worki/squad.json`. Do not edit generated TOML files directly.

Source methodologies are adapted from `msitarzewski/agency-agents` at commit `652b2692f8d8ec2b1f1a38e559073e287dfdc469` under the MIT License. See `LICENSE` and `THIRD_PARTY_NOTICES.md`.
