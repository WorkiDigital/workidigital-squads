# Validação local Worki

Executada em 2026-10-15 com Python 3.12.14.

- `python3 scripts/validate.py`: passou; nove etapas, dez skills, referências às competências originais e licença preservada.
- `python3 -m unittest discover -s tests -v`: dez testes passaram, incluindo fluxo 01–09 e retomada, cliente separado, bloqueios de ordem e evidência, parcial, traversal/symlink, entrega alterada e aprovação ausente/revogada/de outra ação, ambiente ou versão.
- `python3 scripts/worki.py --help`: entrada da CLI disponível.

Fixtures são sintéticas, criadas em diretórios temporários e removidas ao terminar. Nenhuma pesquisa real foi simulada como evidência pública. Não foram executados os testes ou instaladores upstream, LLMs em paralelo, deploy, publicação ou alterações em sites. Qualidade de estratégia, correspondência de claims à fonte e autorização real precisam de revisão pelo assistente/operador com um cliente concreto.

Validação adicional: CLI init/context executada em sandbox temporária; tentativa de avançar para etapa 02 antes de concluir 01 retornou exit code 1 e BLOQUEADO. Comparação byte a byte com o checkout upstream fixado confirmou 381 arquivos originais intactos; somente README e .gitignore têm integração Worki. Novos arquivos Worki ficam separados do catálogo original.
