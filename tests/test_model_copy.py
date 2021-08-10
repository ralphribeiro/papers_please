from src.app.model_copy import (
    Entrante, Papel,
    regra_consistência_documentos,
    regra_valida_data
)


class TestEntrante:
    def test_papel_adicionado_dado_raw(self):
        josef = {"passport": 'ID#: GC07D-FU8AR\nNATION: Arstotzka\nNAME: Costanza, Josef\nDOB: 1933.11.28\nSEX: M\nISS: East Grestin\nEXP: 1983.03.15'}
        entrante = Entrante(josef, [lambda: None])
        passaporte = Papel(josef)
        assert passaporte in entrante.papeis
        assert entrante.papeis[0].nome == 'passport'
        assert entrante.papeis[0].itens['id'] == 'GC07D-FU8AR'

    def test_papeis_adicionados_dado_raw(self):
        roman = {
            "passport": 'ID#: WK9XA-LKM0Q\nNATION: United Federation\nNAME: Dolanski, Roman\nDOB: 1933.01.01\nSEX: M\nISS: Shingleton\nEXP: 1983.05.12',
            "grant_of_asylum": 'NAME: Dolanski, Roman\nNATION: United Federation\nID#: Y3MNC-TPWQ2\nDOB: 1933.01.01\nHEIGHT: 176cm\nWEIGHT: 71kg\nEXP: 1983.09.20'
        }
        entrante = Entrante(roman, [lambda: None])
        papeis = entrante.constroi_papeis(roman)
        for p in papeis:
            assert p in entrante.papeis


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
        assert papel.itens == esperado_items


class TestRegras:
    def test_regra_consistência_documentos_id_diferente(self):
        roman = {
            "passport": 'ID#: WK9XA-LKM0Q\nNATION: United Federation\nNAME: Dolanski, Roman\nDOB: 1933.01.01\nSEX: M\nISS: Shingleton\nEXP: 1983.05.12',
            "grant_of_asylum": 'NAME: Dolanski, Roman\nNATION: United Federation\nID#: Y3MNC-TPWQ2\nDOB: 1933.01.01\nHEIGHT: 176cm\nWEIGHT: 71kg\nEXP: 1983.09.20'
        }
        entrante = Entrante(roman, [regra_consistência_documentos])
        entrante.submete_papeis_regras()
        assert entrante.status == ['Detainment: ID number mismatch.']

    def test_regra_validade_documentos_passaporte_vencido(self):
        josef = {"passport": 'ID#: GC07D-FU8AR\nNATION: Arstotzka\nNAME: Costanza, Josef\nDOB: 1933.11.28\nSEX: M\nISS: East Grestin\nEXP: 1930.03.15'}
        entrante = Entrante(josef, [regra_valida_data])
        entrante.submete_papeis_regras()
        assert entrante.status == ['Entry denied: passport expired.']

    def test_regra_validade_documentos_passaporte_e_asilo_vencidos(self):
        roman = {
            "passport": 'ID#: Y3MNC-TPWQ2\nNATION: United Federation\nNAME: Dolanski, Roman\nDOB: 1933.01.01\nSEX: M\nISS: Shingleton\nEXP: 1912.05.12',
            "grant_of_asylum": 'NAME: Dolanski, Roman\nNATION: United Federation\nID#: Y3MNC-TPWQ2\nDOB: 1933.01.01\nHEIGHT: 176cm\nWEIGHT: 71kg\nEXP: 1900.09.20'
        }
        entrante = Entrante(roman, [regra_valida_data])
        entrante.submete_papeis_regras()
        assert entrante.status == ['Entry denied: passport expired.', 'Entry denied: grant_of_asylum expired.']


class TestBoletim:
    ...
