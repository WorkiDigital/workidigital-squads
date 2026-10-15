"""Read-only checks for the Worki marketing squad; no upstream code execution."""
from pathlib import Path
import json
import re

root = Path(__file__).resolve().parents[1]
state = json.loads((root / 'templates/estado.json').read_text())
assert len(state['etapas']) == 9
for name, entry in state['etapas'].items():
    skill = root / '.agents/skills' / name / 'SKILL.md'
    agent = root / 'agents' / (name + '.md')
    text = skill.read_text()
    assert text.startswith('---\nname: ' + name + '\n')
    assert 'description:' in text and '## Método' in text
    assert entry['arquivo'] in text
    assert 'aprovação' in text and 'evidências' in text
    assert skill.relative_to(root).as_posix() in agent.read_text()
assert (root / '.agents/skills/marketing-squad/SKILL.md').is_file()
assert 'Não altere sites' in (root / 'agents/orquestrador.md').read_text()
for relative in ('AGENTS.md', 'docs/README-squad.md', 'docs/analise-agency-agents.md',
                 'templates/briefing.md', 'templates/aprovacoes.md',
                 'templates/decisoes.md', 'templates/01-evidencias.md',
                 'templates/09-diagnostico-plano.md', 'THIRD_PARTY_NOTICES.md'):
    assert (root / relative).is_file(), relative
for value in ('cliente-a', 'cliente-b', '2026-10-15-01'):
    assert re.fullmatch(r'[a-z0-9][a-z0-9-]*', value)
for value in ('../cliente-b', '/tmp', 'cliente/a', ''):
    assert not re.fullmatch(r'[a-z0-9][a-z0-9-]*', value)
print('PASS: 9 especialistas, 10 skills, referências e modelos do squad consistentes.')
print('Sem execução de scripts upstream, rede, escrita ou pesquisa de clientes.')

registry = json.loads((root / 'worki/squad.json').read_text())
assert [s['id'] for s in registry['stages']] == list(state['etapas'])
assert (root / registry['orchestrator_base']).is_file()
for stage in registry['stages']:
    skill = (root / stage['skill']).read_text()
    for source in stage['agents']:
        assert (root / source).is_file(), source
        assert source in skill, source
    assert stage['output'] == state['etapas'][stage['id']]['arquivo']
license_text = (root / 'LICENSE').read_text()
assert license_text in (root / 'THIRD_PARTY_NOTICES.md').read_text()
print('PASS: agentes originais referenciados, manifesto e licença MIT preservada.')
