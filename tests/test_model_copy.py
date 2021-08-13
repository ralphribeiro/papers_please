from functools import partial

import pytest

from src.app.model_copy import (
    Entrante, Papel,
    regra_consistência_documentos,
    regra_criminal,
    regra_id_card_obrigatório,
    regra_nações_permitidas,
    regra_passaporte_obrigatório,
    regra_vacinação_obrigatória,
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
        assert entrante.status == [
            'Entry denied: passport expired.', 'Entry denied: grant_of_asylum expired.']

    def test_regra_passporte_obrigatório(self):
        roman = {
            "passport": 'ID#: Y3MNC-TPWQ2\nNATION: United Federation\nNAME: Dolanski, Roman\nDOB: 1933.01.01\nSEX: M\nISS: Shingleton\nEXP: 1912.05.12',
            "grant_of_asylum": 'NAME: Dolanski, Roman\nNATION: United Federation\nID#: Y3MNC-TPWQ2\nDOB: 1933.01.01\nHEIGHT: 176cm\nWEIGHT: 71kg\nEXP: 1998.09.20'
        }
        entrante = Entrante(roman, [regra_passaporte_obrigatório])
        entrante.submete_papeis_regras()
        assert entrante.status == []

    def test_regra_passporte_obrigatório_faltante(self):
        roman = {
            "grant_of_asylum": 'NAME: Dolanski, Roman\nNATION: United Federation\nID#: Y3MNC-TPWQ2\nDOB: 1933.01.01\nHEIGHT: 176cm\nWEIGHT: 71kg\nEXP: 1999.09.20'
        }
        entrante = Entrante(roman, [regra_passaporte_obrigatório])
        entrante.submete_papeis_regras()
        assert entrante.status == ['Entry denied: missing required passport.']

    def test_regra_id_card_obrigatório(self):
        brenna = {
            'ID_card': 'NAME: Kierkgaard, Brenna\nDOB: 1952.02.07\nHEIGHT: 179cm\nWEIGHT: 124kg'}
        entrante = Entrante(brenna, [regra_id_card_obrigatório])
        entrante.submete_papeis_regras()
        assert entrante.status == []

    def test_regra_id_card_obrigatório_faltante(self):
        josef = {"passport": 'ID#: GC07D-FU8AR\nNATION: Arstotzka\nNAME: Costanza, Josef\nDOB: 1933.11.28\nSEX: M\nISS: East Grestin\nEXP: 1983.03.15'}
        entrante = Entrante(josef, [regra_id_card_obrigatório])
        entrante.submete_papeis_regras()
        assert entrante.status == ['Entry denied: missing required ID card.']

    def test_regra_vacinação_obrigatória(self):
        lang = {
            "certificate_of_vaccination": 'ID#: K9W1X-DDQNM\nNAME: Lang, Tomasz\nVACCINES: polio, tetanus, cowpox',
            "passport": 'ID#: K9W1X-DDQNM\nNATION: Capela\nNAME: Lang, Tomasz\nDOB: 1933.01.01\nSEX: M\nISS: Shingleton\nEXP: 1990.05.12'
        }
        atualização = {'Capela': ('polio', )}
        regra_v = partial(regra_vacinação_obrigatória, atualização)
        entrante = Entrante(lang, [regra_passaporte_obrigatório, regra_v])
        entrante.submete_papeis_regras()
        assert entrante.status == []

    def test_regra_vacinação_obrigatória_faltante(self):
        lang = {
            "certificate_of_vaccination": 'ID#: K9W1X-DDQNM\nNAME: Lang, Tomasz\nVACCINES: polio, tetanus, cowpox',
            "passport": 'ID#: K9W1X-DDQNM\nNATION: Capela\nNAME: Lang, Tomasz\nDOB: 1933.01.01\nSEX: M\nISS: Shingleton\nEXP: 1990.05.12'
        }
        atualização = {'Capela': ('covid-19', )}
        regra_v = partial(regra_vacinação_obrigatória, atualização)
        entrante = Entrante(lang, [regra_passaporte_obrigatório, regra_v])
        entrante.submete_papeis_regras()
        assert entrante.status == [
            'Entry denied: missing required covid-19 vaccination.'
        ]

    def test_regra_nações_permitidas(self):
        josef = {"passport": 'ID#: GC07D-FU8AR\nNATION: Capela\nNAME: Costanza, Josef\nDOB: 1933.11.28\nSEX: M\nISS: East Grestin\nEXP: 1983.03.15'}
        atualização = {'allow': ('Burned Ranch', 'Peterland', 'Capela', )}
        regra_n = partial(regra_nações_permitidas, atualização)
        entrante = Entrante(josef, [regra_n])
        entrante.submete_papeis_regras()
        assert entrante.status == []

    def test_regra_nações_permitidas_com_nação_negada(self):
        josef = {"passport": 'ID#: GC07D-FU8AR\nNATION: Capela\nNAME: Costanza, Josef\nDOB: 1933.11.28\nSEX: M\nISS: East Grestin\nEXP: 1983.03.15'}
        atualização = {'allow': ('Burned Ranch', 'Peterland', )}
        regra_n = partial(regra_nações_permitidas, atualização)
        entrante = Entrante(josef, [regra_n])
        entrante.submete_papeis_regras()
        assert entrante.status == ['Entry denied: Entrant from Capela.']

    def test_regra_criminal(self):
        josef = {"passport": 'ID#: GC07D-FU8AR\nNATION: Capela\nNAME: Costanza, Josef\nDOB: 1933.11.28\nSEX: M\nISS: East Grestin\nEXP: 1983.03.15'}
        atualização = ('Costanza, Josef', 'Bozo', )
        regra_n = partial(regra_criminal, atualização)
        entrante = Entrante(josef, [regra_n])
        entrante.submete_papeis_regras()
        assert entrante.status == ['Detainment: Entrant is a wanted criminal.']


@pytest.mark.skip('a implementar')
class TestAtualização:
    def test_atualização_nações_permite_entrantes(self):
        entrada = 'Allow citizens of Obristan'
        atualização = AtualizaçãoNações(entrada)
        assert atualização.permitido == ('Obristan', )

    def test_atualização_documentos(self):
        ...

    def test_atualização_vacinação(self):
        ...

    def test_atualização_criminal(self):
        ...
