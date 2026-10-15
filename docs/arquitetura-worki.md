# Arquitetura e plano de implementação Worki

## Proposta

Orquestrador Worki → catálogo existente + contratos de skills → evidências e entregáveis por cliente/run → revisão → pacote de aprovação → execução autorizada por operador/assistente.

O núcleo tem três camadas: catálogo upstream preservado; adaptadores/skills Worki; CLI local Python de estado e verificação. Sem dependências externas, chamadas de modelo automáticas ou serviços persistentes. O host oferece ferramentas e delegação. A CLI prepara contexto e aplica gates documentais; não produz pesquisa ou estratégia por conta própria.

## Mapa de competências reutilizadas

- **01-evidencias**: `research/research-synthesist.md`, `testing/testing-evidence-collector.md`
- **02-concorrentes**: `product/product-trend-researcher.md`, `research/research-synthesist.md`
- **03-posicionamento**: `design/design-brand-guardian.md`, `sales/sales-proposal-strategist.md`
- **04-ofertas**: `sales/sales-offer-lead-gen-strategist.md`
- **05-copywriting**: `marketing/marketing-content-creator.md`
- **06-cro**: `marketing/marketing-growth-hacker.md`, `design/design-ux-researcher.md`
- **07-ux-ui**: `design/design-ux-researcher.md`, `design/design-ux-architect.md`, `design/design-ui-designer.md`
- **08-desenvolvimento**: `engineering/engineering-frontend-developer.md`, `testing/testing-accessibility-auditor.md`
- **09-diagnostico-plano**: `research/research-synthesist.md`, `testing/testing-evidence-collector.md`

Orquestração base: specialized/agents-orchestrator.md. Testing Reality Checker não foi adotado como gate automático, pois contém comandos específicos de stack e scripts que não existem neste projeto. Evidências e síntese cobrem revisão sem assumir essas ferramentas.

## Dados e fluxo

`clients/<cliente>/runs/<run>/` guarda briefing, estado, evidencias.json, relatórios 01–09, metadados de revisão, decisões e aprovações. O manifesto worki/squad.json define ordem, dependências e competências. Evidências precedem todo diagnóstico; fatos referenciam E-IDs do mesmo run. Cada etapa requer a anterior concluída. O retorno inclui resumo, achados, lacunas e caminhos; o revisor aceita ou pede correção.

Os entregáveis culminam em diagnóstico, problemas, oportunidades, priorização e plano 7/30/90 dias. Execução em sites e publicação são bloqueadas por padrão; a CLI não possui executor externo.

## Plano executado

1. Inventariar catálogo e reutilizar competências por referência, preservando fontes e MIT.
2. Acrescentar mapa de papéis, política Worki e contratos estruturados às skills já existentes.
3. Implementar CLI sem dependências para inicialização, contexto, conclusão e conferência de registro de aprovação.
4. Testar fluxo positivo e falhas: ordem das etapas, evidência ausente, cliente trocado, traversal, symlink, aprovação ausente, escopo e versão divergentes.
5. Documentar uso e limites; executar validação local sem instalar upstream, modificar sites ou publicar.
