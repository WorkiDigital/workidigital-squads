# Análise e revisão do agency-agents

Fonte pública: https://github.com/msitarzewski/agency-agents
Commit analisado: 652b2692f8d8ec2b1f1a38e559073e287dfdc469
Consulta: 2026-10-15. Revisão estática direcionada, não auditoria integral ou garantia de segurança.

## Evidências verificáveis

Links abaixo são fixados no commit; localizadores são nomes de seções/funções.

- `SECURITY.md`, Scope: prompts Markdown e scripts de conversão/instalação; recomenda revisão antes de executar.
- `integrations/codex/README.md`, Convert And Install: conversão para TOML e instalação em ~/.codex/agents/; não constitui sandbox ou concessão granular de permissões.
- `scripts/install.sh`, install_file: copia arquivos e pode substituir arquivo regular de destino; --link cria links; há proteção para links não pertencentes ao instalador. ensure_converted executa conversor automaticamente e limpa saídas parciais usando find/rm. Modo padrão pode selecionar todas as ferramentas detectadas.
- `scripts/convert.sh`, convert_codex: copia corpo dos prompts para developer_instructions, sem impor controles de ferramentas; rotinas de geração limpam saídas. É preciso revisar prompts além do shell.
- `integrations/mcp-memory/setup.sh`: apresenta instruções e verifica existência de configurações; não instala um servidor real. Memória compartilhada não garante isolamento por cliente.
- `.github/workflows/test-install.yml`: executa scripts em Linux/macOS; usa actions/checkout@v4. Nos workflows inspecionados não há permissions explícitas; permissões efetivas dependem das configurações do GitHub. Tags de actions não são SHAs imutáveis.
- `specialized/agents-orchestrator.md`: pipeline de desenvolvimento e ciclos dev/QA; precisa de escopo e aprovação explícitos para o contexto da agência.
- `sales/sales-offer-lead-gen-strategist.md`: mecanismos úteis para estruturar ofertas; afirmações genéricas de conversão e benchmarks não são evidência sobre um cliente e não foram adotadas como fatos.
- `design/design-brand-guardian.md`, `design/design-ux-architect.md`, `testing/testing-evidence-collector.md`, `engineering/engineering-frontend-developer.md`: úteis para marca, UX, evidências e desenvolvimento. Metas de performance e exemplos precisam de validação atual; o frontend contém referência a FID, substituído por INP nos Core Web Vitals. Esta adaptação usa medições atuais sem prometer pontuação.

Base para cada caminho: https://github.com/msitarzewski/agency-agents/blob/652b2692f8d8ec2b1f1a38e559073e287dfdc469/

## Decisão

Não executar install.sh, convert.sh, testes ou configuração MCP upstream. Não copiar configurações globais, integrar servidores ou conceder credenciais. O clone de revisão ficou em /tmp, fora dos checkouts de projeto. Foram usados Git para obtenção, leitura estática e ferramentas locais para escrever a adaptação; nenhum script upstream foi executado.

## Adaptação

Criamos um orquestrador, especialistas e skills focados no fluxo de marketing. Preservamos a ideia de papéis especializados e revisão por evidências, acrescentando pesquisa concorrencial, contratos de entrega, controle de claims, isolamento de contexto, rastreabilidade e aprovação de mudanças. Não copiamos o catálogo inteiro nem assumimos que prompts fornecem ferramentas, memória persistente ou execução paralela.

Nenhuma instalação externa é necessária. A execução de pesquisa em clientes depende de URLs reais e acesso público permitido; domínios adicionais devem ser liberados nas configurações quando bloqueados. Analytics e CMS não são pré-requisitos para diagnóstico público; ficam opcionais e sujeitos a autorização. Não há diagnóstico real de cliente sem briefing.

## Licença

Upstream MIT, copyright 2025 AgentLand Contributors. A licença e atribuição estão preservadas em THIRD_PARTY_NOTICES.md. Esta revisão não concede direitos sobre marcas, sites ou materiais de clientes.

## Importação solicitada para a Worki

Após a revisão, o usuário solicitou a cópia completa para seu repositório. Foram importados os 383 arquivos versionados do commit acima na raiz de workidigital-squads, sem copiar o .git de origem ou executar scripts. O origin continua WorkiDigital/workidigital-squads; upstream referencia msitarzewski/agency-agents. O histórico upstream não foi importado. README.md recebeu navegação para o squad e .gitignore recebeu exclusões para dados de clientes; os outros 381 arquivos foram conferidos byte a byte. O guia original do squad ficou em docs/README-squad.md. Workflows upstream também foram copiados: antes de futuro push ou ativação de CI, revise permissões efetivas, actions e execução dos scripts; a revisão estática direcionada não aprova automaticamente toda essa automação.

Validação executada: python3 scripts/validate.py (estrutura e referências), mais comparação da importação com o checkout fixado. Não foram executados testes upstream, ensaio comportamental de assistente ou diagnóstico de cliente. Não houve commit, push, instalação global, publicação ou alteração de sites.


## Evolução para o sistema Worki

A versão atual reutiliza competências por referências verificadas em worki/squad.json. Adaptadores e skills acrescentam contratos locais; as fontes do catálogo e LICENSE permanecem intactas. Inclui CLI Python sem dependências externas, sem rede, subprocessos ou executor de sites/deploy. Revisão local dos novos scripts: init escreve apenas contexto do run; context retorna caminhos filtrados; complete valida sidecars e fingerprints de entregas; check-approval consulta registros sem executar a ação. IDs e caminhos são validados; symlinks e traversal são recusados. Isso não substitui sandbox do host nem autentica aprovação ou veracidade de pesquisa.

Os workflows upstream não foram ativados nem executados; instalação global, MCP e scripts de conversão continuam fora do fluxo padrão. Não foi necessário instalar dependências. Os controles de aprovação são registro e política operacional, não um sistema de identidade. Para barreiras reais entre clientes, aplicar ambientes e credenciais separados.
