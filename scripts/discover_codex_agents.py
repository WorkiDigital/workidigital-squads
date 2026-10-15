#!/usr/bin/env python3
"""Discover and validate project-scoped Worki Codex agents."""

from __future__ import annotations

import argparse
import json
from pathlib import Path
import tomllib


ROOT = Path(__file__).resolve().parents[1]


def discover() -> list[dict[str, str]]:
    agents_dir = ROOT / ".codex/agents"
    if not agents_dir.is_dir():
        raise RuntimeError(".codex/agents não existe")
    agents = []
    names = set()
    for path in sorted(agents_dir.glob("*.toml")):
        data = tomllib.loads(path.read_text(encoding="utf-8"))
        for key in ("name", "description", "developer_instructions"):
            if not isinstance(data.get(key), str) or not data[key].strip():
                raise ValueError(f"{path}: campo obrigatório inválido: {key}")
        if data["name"] in names:
            raise ValueError(f"Nome duplicado: {data['name']}")
        names.add(data["name"])
        agents.append({
            "name": data["name"],
            "description": data["description"],
            "path": str(path.relative_to(ROOT)),
        })
    if not agents:
        raise RuntimeError("Nenhum agente descoberto")
    return agents


def main() -> None:
    parser = argparse.ArgumentParser(description=__doc__)
    parser.add_argument("--json", action="store_true")
    args = parser.parse_args()
    agents = discover()
    if args.json:
        print(json.dumps({"count": len(agents), "agents": agents}, ensure_ascii=False, indent=2))
    else:
        print(f"PASS: {len(agents)} Codex agents discovered")
        for agent in agents:
            print(f"- {agent['name']}: {agent['path']}")


if __name__ == "__main__":
    main()
