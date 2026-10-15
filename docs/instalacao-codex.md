# Instalação do squad no Codex

O squad da Worki Digital é instalado no próprio projeto. Os agentes executáveis ficam em `.codex/agents/*.toml`; o catálogo em `worki/codex-agents.json` define o nome, as fontes originais e a skill atribuída a cada papel.

## Agentes instalados

| Agente | Responsabilidade |
| --- | --- |
| Worki Marketing Orchestrator | Isolamento de contexto, ordem das etapas, gates e delegação |
| Worki Evidence Researcher | Coleta e classificação de evidências públicas verificáveis |
| Worki Competitive Analyst | Mercado, concorrentes e lacunas competitivas |
| Worki Brand Positioning Strategist | Posicionamento, diferenciação e mensagens |
| Worki Offer Architect | Diagnóstico e reconstrução de ofertas |
| Worki Conversion Copywriter | Copy para páginas, anúncios e mensagens comerciais |
| Worki CRO Specialist | Diagnóstico de conversão e experimentos priorizados |
| Worki UX UI Specialist | Arquitetura de informação, fluxos e especificação visual |
| Worki Website Developer | Planejamento e implementação revisável de sites |
| Worki Diagnostic Reviewer | Revisão das evidências, riscos e plano de execução |

Cada TOML incorpora as instruções dos especialistas selecionados do `agency-agents`, a skill Worki da etapa, a política de aprovação e a atribuição de origem. O conteúdo upstream permanece licenciado nos termos de `LICENSE`; os detalhes de procedência estão em `THIRD_PARTY_NOTICES.md`.

## Gerar e descobrir

Depois de alterar uma fonte, regenere os arquivos:

```bash
python3 scripts/generate_codex_agents.py
```

Confira se o repositório contém exatamente os arquivos esperados e se todos são TOML válidos:

```bash
python3 scripts/generate_codex_agents.py --check
python3 scripts/discover_codex_agents.py
```

O primeiro comando detecta diferenças entre as fontes e os artefatos instalados. O segundo simula a descoberta do projeto, valida os campos exigidos e mostra os nomes que podem ser delegados. `AGENTS.md` orienta novas sessões a carregar primeiro `Worki Marketing Orchestrator` e a usar o manifesto como roster autorizado.

## Fluxo operacional

1. Crie um run separado com `python3 scripts/worki.py init <cliente> <run> --domain <url> --goal <objetivo>`.
2. Carregue `.codex/agents/worki-marketing-orchestrator.toml`.
3. O orquestrador executa a descoberta e delega a cada especialista pelo nome exato.
4. Cada entrega usa somente o contexto do cliente e do run informados.
5. Alterações em sites exigem aprovação explícita; publicação e implantação exigem nova aprovação.

Os dados reais em `clients/` são ignorados pelo Git. Versione apenas templates e exemplos fictícios.

## Validação completa

```bash
python3 scripts/validate.py
python3 -m unittest discover -s tests -v
git diff --check
```

O workflow `.github/workflows/validate-worki-squad.yml` repete a geração em modo de verificação, a descoberta e os testes em cada Pull Request e push para `main`. Todos os workflows usam permissão somente de leitura para o conteúdo do repositório.
