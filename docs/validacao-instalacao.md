# Validação da instalação

Data: 2026-10-15

## Descoberta

`python3 scripts/discover_codex_agents.py --json` encontrou e carregou os 10 TOMLs esperados em `.codex/agents/`. Os testes confirmam nomes únicos, campos obrigatórios, vínculo de cada etapa com um agente, fontes upstream incorporadas, skill correspondente, política de aprovação e aviso de licença.

## Delegação

Um subagente isolado recebeu `.codex/agents/worki-evidence-researcher.toml` e a alegação fictícia “Somos líderes”, publicada no próprio site da empresa e sem fonte independente. O agente:

- identificou-se como `Worki Evidence Researcher`;
- classificou a frase como declaração da própria fonte;
- recusou tratá-la como fato verificável;
- informou as fontes-base `research/research-synthesist.md` e `testing/testing-evidence-collector.md`.

Esse resultado confirma que as instruções agregadas no TOML são utilizáveis em uma delegação real e preservam a regra de evidência antes do diagnóstico.

## Testes locais

- Gerador em modo `--check`: 10 agentes atuais, sem divergência.
- Validador Worki: 9 especialistas, 10 skills, referências, templates e licença consistentes.
- Testes Python: 14 aprovados, incluindo isolamento entre clientes, traversal, symlinks, dependências, evidências, integridade de artefato e escopo de aprovações.
- Validadores upstream: 18 divisões, 4 runbooks, 64 referências de agentes e 17 integrações consistentes.
- Testes do instalador upstream: 66 aprovados, 0 falhas e 2 casos `xfail` já documentados pelo projeto original.
- Verificação de whitespace nos arquivos Worki e nas configurações alteradas: `git diff --check` sem erros. O catálogo upstream foi mantido byte a byte e conserva formatação histórica própria.

Os testes do instalador usam diretórios temporários. Nenhum site, serviço, campanha ou infraestrutura externa foi alterado ou publicado.
