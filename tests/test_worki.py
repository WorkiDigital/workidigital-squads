"""Behavioral workflow tests with synthetic data only; no external requests."""
import copy
import importlib.util
import json
from pathlib import Path
import shutil
import tempfile
import unittest

ROOT = Path(__file__).resolve().parents[1]
spec = importlib.util.spec_from_file_location('worki', ROOT / 'scripts/worki.py')
w = importlib.util.module_from_spec(spec)
spec.loader.exec_module(w)


class WorkflowTests(unittest.TestCase):
    def setUp(self):
        self.tmp = tempfile.TemporaryDirectory()
        self.addCleanup(self.tmp.cleanup)
        self.root = Path(self.tmp.name)
        for directory in ('worki', 'templates'):
            shutil.copytree(ROOT / directory, self.root / directory)
        self.flow = w.Workflow(self.root)
        for client in ('cliente-a', 'cliente-b'):
            self.flow.init(client, 'run-01', 'https://example.com', 'Diagnóstico fictício para teste')
        self.folder = self.flow.run('cliente-a', 'run-01')
        self.rows = [{'id': 'E001', 'cliente': 'cliente-a', 'run': 'run-01',
                      'url': 'https://example.com', 'capturado_em': '2026-10-15T10:00:00-03:00',
                      'trecho': 'Observação sintética, sem alegar coleta real',
                      'tipo_fonte': 'fixture de teste', 'limitacoes': 'Não é pesquisa real'}]
        w.save(self.folder / 'evidencias.json', self.rows)

    def deliver(self, stage):
        meta = {'cliente': 'cliente-a', 'run': 'run-01', 'etapa': stage,
                'status': 'concluido', 'resumo': 'Entrega sintética', 'lacunas': [],
                'claims': [{'texto': 'Observação de teste', 'tipo': 'fato', 'evidencias': ['E001']}],
                'revisao': {'responsavel': 'Revisor fictício', 'data': '2026-10-15T10:10:00-03:00', 'parecer': 'aprovado'}}
        w.save(self.folder / (stage + '.json'), meta)
        (self.folder / self.flow.stages[stage]['output']).write_text('Relatório sintético para teste de contrato.\n')
        return meta

    def test_full_workflow_and_resume(self):
        for stage in self.flow.stages:
            context = self.flow.context('cliente-a', 'run-01', stage)
            self.assertTrue(all('/cliente-a/runs/run-01/' in p for p in context['entradas']))
            self.assertNotIn('cliente-b', json.dumps(context))
            self.deliver(stage)
            self.assertEqual(self.flow.complete('cliente-a', 'run-01', stage)['status'], 'concluido')
        resumed = w.Workflow(self.root)
        _, state = resumed.state('cliente-a', 'run-01')
        self.assertTrue(all(s['status'] == 'concluido' for s in state['etapas'].values()))
        _, other = resumed.state('cliente-b', 'run-01')
        self.assertTrue(all(s['status'] == 'pendente' for s in other['etapas'].values()))

    def test_dependency_gate(self):
        with self.assertRaises(ValueError):
            self.flow.context('cliente-a', 'run-01', '02-concorrentes')

    def test_no_overwrite(self):
        with self.assertRaises(FileExistsError):
            self.flow.init('cliente-a', 'run-01', 'https://example.com', 'Novo objetivo')

    def test_traversal_and_symlinks(self):
        for client in ('../cliente-b', '/tmp', 'a/b'):
            with self.assertRaises(ValueError):
                self.flow.run(client, 'run-01')
        (self.root / 'clients/atalho').symlink_to(self.root / 'clients/cliente-b', target_is_directory=True)
        with self.assertRaises(ValueError):
            self.flow.run('atalho', 'run-01')
        (self.folder / 'atalho.json').symlink_to(self.root / 'clients/cliente-b/runs/run-01/estado.json')
        with self.assertRaises(ValueError):
            w.safe(self.folder, 'atalho.json')

    def test_no_facts_without_references(self):
        meta = self.deliver('01-evidencias')
        meta['claims'][0]['evidencias'] = []
        w.save(self.folder / '01-evidencias.json', meta)
        with self.assertRaises(ValueError):
            self.flow.complete('cliente-a', 'run-01', '01-evidencias')
        meta['claims'][0]['evidencias'] = ['E999']
        w.save(self.folder / '01-evidencias.json', meta)
        with self.assertRaises(ValueError):
            self.flow.complete('cliente-a', 'run-01', '01-evidencias')

    def test_foreign_evidence_and_state(self):
        rows = copy.deepcopy(self.rows)
        rows[0]['cliente'] = 'cliente-b'
        w.save(self.folder / 'evidencias.json', rows)
        with self.assertRaises(ValueError):
            self.flow.evidence(self.folder, 'cliente-a', 'run-01')
        state = w.load(self.folder / 'estado.json')
        state['cliente'] = 'cliente-b'
        w.save(self.folder / 'estado.json', state)
        with self.assertRaises(ValueError):
            self.flow.state('cliente-a', 'run-01')

    def test_invalid_or_empty_evidence(self):
        for key, value in (('capturado_em', '2026-10-15'), ('url', 'http://127.0.0.1/'),
                           ('url', 'https://user:secret@example.com'), ('trecho', '')):
            rows = copy.deepcopy(self.rows)
            rows[0][key] = value
            w.save(self.folder / 'evidencias.json', rows)
            with self.assertRaises(ValueError):
                self.flow.evidence(self.folder, 'cliente-a', 'run-01')
        w.save(self.folder / 'evidencias.json', [])
        with self.assertRaises(ValueError):
            self.flow.evidence(self.folder, 'cliente-a', 'run-01')

    def test_partial_blocks_next_stage(self):
        meta = self.deliver('01-evidencias')
        meta.update(status='parcial', lacunas=['Fonte inacessível'])
        meta['revisao']['parecer'] = 'pendente'
        w.save(self.folder / '01-evidencias.json', meta)
        self.assertEqual(self.flow.complete('cliente-a', 'run-01', '01-evidencias')['status'], 'parcial')
        with self.assertRaises(ValueError):
            self.flow.context('cliente-a', 'run-01', '02-concorrentes')

    def test_changed_completed_artifact_blocks_handoff(self):
        self.deliver('01-evidencias')
        self.flow.complete('cliente-a', 'run-01', '01-evidencias')
        (self.folder / '01-evidencias.md').write_text('Mudou após revisão')
        with self.assertRaises(ValueError):
            self.flow.context('cliente-a', 'run-01', '02-concorrentes')

    def test_approval_action_scope_version(self):
        artifact = self.folder / 'proposta.md'
        artifact.write_text('Versão 1')
        def check(action='implementar', environment='local'):
            return self.flow.check_approval('cliente-a', 'run-01', action, 'proposta.md', environment)
        with self.assertRaises(ValueError):
            check()
        row = {'cliente': 'cliente-a', 'run': 'run-01', 'acao': 'implementar',
               'artefato': 'proposta.md', 'sha256': w.digest(artifact), 'ambiente': 'local',
               'status': 'aprovado', 'aprovador': 'Usuário fictício',
               'referencia_mensagem': 'Fixture, não autorização real', 'data': '2026-10-15T10:00:00-03:00'}
        w.save(self.folder / 'aprovacoes.json', [row])
        self.assertTrue(check()['registro_compativel'])
        for action in ('publicar', 'implantar'):
            with self.assertRaises(ValueError):
                check(action)
        with self.assertRaises(ValueError):
            check(environment='producao')
        revoked = dict(row, status='revogado')
        w.save(self.folder / 'aprovacoes.json', [row, revoked])
        with self.assertRaises(ValueError):
            check()
        w.save(self.folder / 'aprovacoes.json', [row])
        artifact.write_text('Versão 2')
        with self.assertRaises(ValueError):
            check()


if __name__ == '__main__':
    unittest.main()
