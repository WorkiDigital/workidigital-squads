# Operação local do squad

Requer Python 3.9+ para a CLI (validado com 3.12), um assistente com acesso ao checkout e ferramentas de pesquisa pública para um trabalho real. Nenhum pacote externo é instalado; não execute scripts/install.sh ou scripts/convert.sh. CLI, testes e validador Worki usam somente biblioteca padrão. O catálogo original continua disponível e seus scripts não fazem parte do fluxo padrão.

## Inicializar e retomar

Na raiz /workspace/workidigital-squads:

```bash
python3 scripts/worki.py init cliente-acme run-01 --domain https://dominio-real-do-cliente.example --goal "Aumentar leads qualificados"
python3 scripts/worki.py context cliente-acme run-01 01-evidencias
```

Substitua o domínio de exemplo pelo domínio confirmado. A inicialização recusa run existente. Complete o briefing e execute o orquestrador com os arquivos indicados no contexto. `context` não chama modelo ou faz pesquisa: retorna o pacote de caminhos para o assistente carregar. Sem ferramenta de delegação, o mesmo assistente executa os papéis sequencialmente e informa essa condição. O manifesto é a fonte dos papéis reutilizados.

Para retomar, leia estado.json do run e use context para a primeira etapa aberta. A CLI recusa contexto de etapa com antecessora não concluída. Não tente resolver bloqueio marcando status manualmente; corrija a entrega e a revisão, ou abra novo run em revisões de conclusões anteriores. Não ler outros clientes ao retomar.

## Evidências

A etapa 01 entrega 01-evidencias.md e evidencias.json. Registro estruturado mínimo (exemplo sintático fictício):

```json
[
  {
    "id": "E001",
    "cliente": "cliente-acme",
    "run": "run-01",
    "url": "https://dominio-real-do-cliente.example/servicos",
    "capturado_em": "2026-10-15T10:00:00-03:00",
    "trecho": "Substituir por trecho literal ou observação realmente coletada",
    "tipo_fonte": "Página oficial do cliente",
    "limitacoes": "Declaração comercial; não comprova resultado de clientes"
  }
]
```

Não use esse exemplo como evidência real. O registro Markdown inclui título, localização e artefatos para auditoria. A validação HTTP(S) é sintática: a CLI não faz requisições nem verifica DNS. A ferramenta de pesquisa precisa respeitar rede, redirecionamentos e bloqueios. URLs oficiais não bastam para provar alegações de resultados; o revisor avalia suporte, independência e atualidade.

## Entrega e passagem de etapa

Cada etapa produz seu relatório e `<etapa>.json`; copie templates/etapa.json para preencher o sidecar. Campos obrigatórios: cliente, run, etapa, status, resumo, claims, lacunas e revisao. Tipos de claim: fato, declaracao, inferencia, hipotese. Evidencias é uma lista de E-IDs do mesmo run; obrigatória e não vazia para fato e declaracao.

```json
{
  "cliente": "cliente-acme",
  "run": "run-01",
  "etapa": "01-evidencias",
  "status": "parcial",
  "resumo": "Pesquisa parcial aguardando confirmação",
  "claims": [{"texto": "Hipótese ainda não validada", "tipo": "hipotese", "evidencias": []}],
  "lacunas": ["Confirmar fontes essenciais"],
  "revisao": {"responsavel": "Nome do revisor", "data": "2026-10-15T10:10:00-03:00", "parecer": "pendente"}
}
```

```bash
python3 scripts/worki.py complete cliente-acme run-01 01-evidencias
```

Um relatório parcial pode ser registrado, mas não libera a próxima etapa. Para concluir, a revisão precisa estar aprovada e sem lacunas pendentes no escopo acordado; limitações aceitas continuam descritas no relatório. Toda conclusão exige ao menos um claim. A CLI confere identidade, E-IDs, metadados, existência do relatório e dependências, e grava hashes dos arquivos revisados. Alterações posteriores em entregas anteriores bloqueiam o próximo handoff. Hashes não autenticam revisão nem detectam fraude por quem pode editar estado e arquivos simultaneamente.

## Aprovação de execução

Entregue proposta concreta e versionada antes de pedir decisão. Em aprovacoes.md mantenha riscos, escopo detalhado, critérios e rollback. Em aprovacoes.json registre só decisões explícitas realmente recebidas do usuário autorizado, com estas chaves:

`cliente`, `run`, `acao` (implementar/publicar/implantar), `artefato` (caminho relativo dentro do run), `sha256` (hash do artefato aprovado), `ambiente`, `status` (aprovado/revogado), `aprovador`, `referencia_mensagem`, `data` (ISO com fuso).

```bash
python3 scripts/worki.py check-approval cliente-acme run-01 --action implementar --artifact proposta.md --environment local
```

A última decisão registrada para o mesmo cliente/run/ação/artefato/ambiente prevalece. Uma revogação invalida a aprovação anterior. Mudança do artefato exige nova aprovação. Aprovar implementar não aprova publicar ou implantar. Mesmo com registro compatível, confira a mensagem original e o escopo antes de executar qualquer ferramenta. A CLI não autentica o aprovador, não escreve código de site e não publica nada. Host e operador continuam responsáveis por impedir ferramentas não autorizadas.

## Validação

```bash
python3 scripts/validate.py
python3 -m unittest discover -s tests -v
```

Os testes usam clientes fictícios em diretórios temporários e não fazem rede, instalações ou alterações de sites. Cobrem fluxo 01–09, retomada, bloqueios de evidência/dependência, isolamento operacional e registros de aprovação. Para pesquisa e estratégia reais, revise fontes e execute o roteiro de examples/ensaio.md com um cliente real autorizado. Não declarar aprovação comercial ou publicação a partir de testes de fixture.
