"""Worki workflow control. Standard library only; no network or external executor."""
import argparse
import hashlib
import ipaddress
import json
from pathlib import Path
import re
from datetime import datetime
from urllib.parse import urlsplit

ROOT = Path(__file__).resolve().parents[1]


def require(ok, message):
    if not ok:
        raise ValueError(message)


def safe(base, relative):
    base = Path(base)
    rel = Path(relative)
    require(not rel.is_absolute() and '..' not in rel.parts, 'Caminho inválido')
    current = base
    require(not current.is_symlink(), 'Symlink recusado')
    for part in rel.parts:
        current = current / part
        require(not current.is_symlink(), 'Symlink recusado')
    require(current.resolve().is_relative_to(base.resolve()), 'Caminho fora da raiz')
    return current


def identity(value):
    require(re.fullmatch(r'[a-z0-9][a-z0-9-]{0,79}', value), 'ID inválido')
    return value


def load(path):
    return json.loads(path.read_text())


def save(path, value):
    path.write_text(json.dumps(value, ensure_ascii=False, indent=2) + '\n')


def stamp(value):
    require(isinstance(value, str), 'Data ausente')
    date = datetime.fromisoformat(value.replace('Z', '+00:00'))
    require(date.tzinfo is not None, 'Data exige fuso')
    return date


def public_url(value):
    url = urlsplit(value)
    require(url.scheme in ('http', 'https') and url.hostname and not url.username
            and not url.password, 'URL pública HTTP(S) exigida')
    host = url.hostname.lower()
    require('.' in host and host != 'localhost' and not host.endswith(('.localhost', '.local', '.internal')), 'Host público exigido')
    try:
        addr = ipaddress.ip_address(host)
    except ValueError:
        pass
    else:
        require(addr.is_global, 'IP privado recusado')
    return value


def meaningful(value):
    return isinstance(value, str) and bool(value.strip()) and 'PREENCHER' not in value


def digest(path):
    return hashlib.sha256(path.read_bytes()).hexdigest()


class Workflow:
    def __init__(self, root=ROOT):
        self.root = Path(root)
        self.registry = load(safe(self.root, 'worki/squad.json'))
        self.stages = {s['id']: s for s in self.registry['stages']}

    def run(self, client, run):
        return safe(self.root, f'clients/{identity(client)}/runs/{identity(run)}')

    def state(self, client, run):
        folder = self.run(client, run)
        state = load(safe(folder, 'estado.json'))
        require(state['cliente'] == client and state['run'] == run, 'Contexto de outro cliente/run')
        return folder, state

    def init(self, client, run, domain, goal):
        public_url(domain)
        require(meaningful(goal), 'Objetivo obrigatório')
        folder = self.run(client, run)
        folder.mkdir(parents=True, exist_ok=False)
        state = load(safe(self.root, 'templates/estado.json'))
        state.update(cliente=client, run=run, dominio=domain, objetivo=goal)
        save(folder / 'estado.json', state)
        for name in ('briefing.md', 'decisoes.md', 'aprovacoes.md', 'aprovacoes.json', 'evidencias.json'):
            (folder / name).write_text(safe(self.root, 'templates/' + name).read_text())
        with (folder / 'briefing.md').open('a') as output:
            output.write(f'\nCliente: {client}\nRun: {run}\nDomínio: {domain}\nObjetivo: {goal}\n')
        return {'run': str(folder), 'status': 'inicializado'}

    def stage(self, stage):
        require(stage in self.stages, 'Etapa desconhecida')
        return self.stages[stage]

    def prerequisites(self, folder, state, stage):
        # Check all previous stages and immutable completion fingerprints.
        for spec in self.registry['stages']:
            if spec['id'] == stage:
                break
            previous = state['etapas'][spec['id']]
            require(previous['status'] == 'concluido', 'Etapa anterior ainda aberta: ' + spec['id'])
            for name, expected in previous['hashes'].items():
                require(digest(safe(folder, name)) == expected, 'Entrega anterior mudou; revalidar em novo run')

    def context(self, client, run, stage):
        folder, state = self.state(client, run)
        spec = self.stage(stage)
        self.prerequisites(folder, state, stage)
        inputs = ['briefing.md', 'estado.json', 'decisoes.md']
        for previous in self.registry['stages']:
            if previous['id'] == stage:
                break
            inputs += [previous['output'], previous['id'] + '.json']
        if stage != '01-evidencias':
            inputs += ['evidencias.json']
        return {'cliente': client, 'run': run, 'etapa': stage,
                'regras': [str(safe(self.root, p)) for p in ('AGENTS.md', 'docs/politica-worki.md')],
                'agentes_base': [str(safe(self.root, p)) for p in spec['agents']],
                'skill': str(safe(self.root, spec['skill'])),
                'entradas': [str(safe(folder, p)) for p in inputs],
                'saidas': [str(safe(folder, spec['output'])), str(safe(folder, stage + '.json'))],
                'permissoes': 'leitura pública e propostas locais; sem alterações de sites/publicação/implantação'}

    def evidence(self, folder, client, run):
        rows = load(safe(folder, 'evidencias.json'))
        require(isinstance(rows, list) and len(rows) > 0, 'Pesquisa sem evidências')
        ids = set()
        for row in rows:
            require(row['cliente'] == client and row['run'] == run, 'Evidência de outro cliente/run')
            require(re.fullmatch(r'E[0-9]{3,}', row['id']) and row['id'] not in ids, 'ID de evidência inválido/duplicado')
            ids.add(row['id'])
            public_url(row['url'])
            stamp(row['capturado_em'])
            require(meaningful(row['trecho']) and meaningful(row['tipo_fonte']), 'Evidência sem observação/origem')
            require(isinstance(row['limitacoes'], str), 'Limitações devem ser explícitas')
        return ids

    def complete(self, client, run, stage):
        folder, state = self.state(client, run)
        spec = self.stage(stage)
        self.prerequisites(folder, state, stage)
        require(state['etapas'][stage]['status'] != 'concluido', 'Etapa já concluída; abra novo run para revisão')
        ids = self.evidence(folder, client, run)
        meta = load(safe(folder, stage + '.json'))
        require((meta['cliente'], meta['run'], meta['etapa']) == (client, run, stage), 'Metadados de outro contexto')
        require(meta['status'] in ('concluido', 'parcial'), 'Status de entrega inválido')
        require(meaningful(meta['resumo']), 'Resumo obrigatório')
        require(isinstance(meta['lacunas'], list), 'Lacunas devem ser uma lista')
        review = meta['revisao']
        require(meaningful(review['responsavel']), 'Revisor obrigatório')
        stamp(review['data'])
        require(review['parecer'] in ('aprovado', 'pendente', 'reprovado'), 'Parecer inválido')
        require(meta['claims'] and isinstance(meta['claims'], list), 'Claims obrigatórios')
        for claim in meta['claims']:
            require(meaningful(claim['texto']), 'Claim vazio')
            require(claim['tipo'] in ('fato', 'declaracao', 'inferencia', 'hipotese'), 'Tipo de claim inválido')
            refs = claim['evidencias']
            require(isinstance(refs, list) and all(ref in ids for ref in refs), 'Referência de evidência inexistente')
            if claim['tipo'] in ('fato', 'declaracao'):
                require(refs, 'Claim factual sem evidência')
        report = safe(folder, spec['output'])
        require(meaningful(report.read_text()), 'Relatório ausente/vazio')
        if meta['status'] == 'concluido':
            require(review['parecer'] == 'aprovado' and not meta['lacunas'], 'Revisão ou lacunas pendentes')
        entry = state['etapas'][stage]
        entry.update(status=meta['status'], bloqueio=meta['lacunas'],
                     hashes={name: digest(safe(folder, name)) for name in
                             (spec['output'], stage + '.json', 'evidencias.json')})
        state['proxima_acao'] = 'Revisar lacunas' if meta['status'] == 'parcial' else 'Consultar próxima etapa ou pacote de aprovação'
        save(safe(folder, 'estado.json'), state)
        return {'etapa': stage, 'status': meta['status'], 'verificacao': 'contrato estrutural; veracidade exige revisão'}

    def check_approval(self, client, run, action, artifact, environment):
        require(action in ('implementar', 'publicar', 'implantar'), 'Ação inválida')
        folder, _ = self.state(client, run)
        path = safe(folder, artifact)
        sha = digest(path)
        # Last recorded decision for this scope wins, including revocation.
        for row in reversed(load(safe(folder, 'aprovacoes.json'))):
            if (row.get('cliente'), row.get('run'), row.get('acao'), row.get('artefato'),
                row.get('ambiente')) != (client, run, action, artifact, environment):
                continue
            require(row.get('status') == 'aprovado' and row.get('sha256') == sha,
                    'Última decisão revogada, pendente ou de outra versão')
            require(meaningful(row.get('aprovador')) and meaningful(row.get('referencia_mensagem')), 'Aprovação sem origem verificável')
            stamp(row['data'])
            return {'registro_compativel': True, 'sha256': sha,
                    'aviso': 'Conferir mensagem original e revogações antes de agir. Nenhuma ação executada.'}
        raise ValueError('Sem registro de aprovação correspondente à ação, cliente, run, ambiente e versão')


def main():
    parser = argparse.ArgumentParser(description=__doc__)
    sub = parser.add_subparsers(dest='command', required=True)
    for name in ('init', 'context', 'complete', 'check-approval'):
        cmd = sub.add_parser(name)
        cmd.add_argument('client')
        cmd.add_argument('run')
        if name in ('context', 'complete'):
            cmd.add_argument('stage')
        if name == 'init':
            cmd.add_argument('--domain', required=True)
            cmd.add_argument('--goal', required=True)
        if name == 'check-approval':
            cmd.add_argument('--action', choices=('implementar', 'publicar', 'implantar'), required=True)
            cmd.add_argument('--artifact', required=True)
            cmd.add_argument('--environment', required=True)
    args = vars(parser.parse_args())
    command = args.pop('command').replace('-', '_')
    try:
        result = getattr(Workflow(), command)(**args)
    except (ValueError, OSError, KeyError, TypeError) as error:
        parser.exit(1, 'BLOQUEADO: ' + str(error) + '\n')
    print(json.dumps(result, ensure_ascii=False, indent=2))


if __name__ == '__main__':
    main()
