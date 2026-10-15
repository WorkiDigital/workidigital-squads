# Squad de diagnóstico e execução de marketing

Squad em português, adaptado criticamente do agency-agents. Funciona por instruções de agentes e skills Markdown; não requer npm, serviços, credenciais ou instaladores globais. Requer um assistente com leitura de arquivos e acesso público à web para pesquisa real. Não é um serviço autônomo que fica em execução.

## Iniciar

Na raiz do checkout, use:

> Use a skill marketing-squad e agents/orquestrador.md para o cliente acme, domínio https://dominio-do-cliente.example, objetivo aumentar leads qualificados. Crie um novo run; pesquise evidências públicas antes de diagnosticar. Não altere sites nem publique.

Substitua o domínio de exemplo pelo real. Inicialize com `python3 scripts/worki.py init <cliente> <run> --domain https://dominio-real --goal "objetivo"`. O comando cria contexto separado sem sobrescrever runs. Consulte [a instalação dos agentes Codex](instalacao-codex.md), [a arquitetura](arquitetura-worki.md), [a operação da CLI](operacao-worki.md) e [a política Worki](politica-worki.md). Nenhum diagnóstico real de cliente está incluído nesta configuração.

## Papéis e etapas

01 evidências → 02 concorrentes → 03 posicionamento → 04 ofertas → 05 copywriting → 06 CRO → 07 UX/UI → 08 desenvolvimento → 09 diagnóstico e plano. As competências são reutilizadas do catálogo original conforme `worki/squad.json`. Os adaptadores locais não recriam personas. O orquestrador delega quando o host suporta ou executa papéis sequencialmente, com revisão de gates.

Entregas: diagnóstico atual, problemas com evidências, oportunidades, recomendações priorizadas e plano 7/30/90 dias; propostas de oferta, copy, UX e implementação ficam disponíveis para revisão. Falta de analytics limita CRO a hipóteses e desenho de experimentos.

## Aprovações e contexto

Cada run guarda briefing, evidências, entregáveis, estado, decisões e aprovações. Nunca misture clientes. Mudanças em sites e execução de código para sites aguardam aprovação explícita; publicação exige aprovação separada. Veja AGENTS.md e templates/aprovacoes.md. Isso é controle por instruções, não substitui restrições de ferramentas e acessos do host.

## Validar

`python3 scripts/generate_codex_agents.py --check`, `python3 scripts/discover_codex_agents.py`, `python3 scripts/validate.py` e `python3 -m unittest discover -s tests -v`

O validador verifica estrutura e referências; os testes exercitam o fluxo local e os bloqueios com dados fictícios. Nenhum deles valida qualidade de estratégia ou resultados comerciais. Para teste de fluxo, veja examples/ensaio.md. Não há dependências externas a instalar. Arquivos de clientes são ignorados pelo Git; faça backup privado seguro quando necessário.
