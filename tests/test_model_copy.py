from src.app.model_copy import Papel


class TestEntrante:
    def test_papeis_sanitizatos_dado_raw(self):
        # assert entrante.papeis == 1
        ...


class TestPapel:
    def test_sanitiza_papeis(self):
        josef = {"passport": 'ID#: GC07D-FU8AR\nNATION: Arstotzka\nNAME: Costanza, Josef\nDOB: 1933.11.28\nSEX: M\nISS: East Grestin\nEXP: 1983.03.15'}
        papel = Papel(josef)
        esperado_nome = 'passport'
        esperado_items = {
            'id': 'GC07D-FU8AR',
            'nation': 'Arstotzka',
            'name': 'Costanza, Josef',
            'dob': '1933.11.28',
            'sex': 'M',
            'iss': 'East Grestin',
            'exp': '1983.03.15'
        }
        assert papel.nome == esperado_nome
        assert papel.items == esperado_items
