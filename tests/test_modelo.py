from pytest import mark

from src.app.modelo import (
    Inspetor, Boletim, regra_consistência_documentos, regra_passaporte, sanitiza_papeis
)


class TestBoletim:
    def test_recebe_boletim_constrói_boletim(self):
        boletim_raw = """Entrants require passport
                        Allow citizens of Arstotzka, Obristan"""
        boletim = Boletim(boletim_raw)
        inspetor = Inspetor()
        inspetor.recebe_boletim(boletim_raw)
        assert boletim in inspetor.boletins


class TestRegras:
    @mark.skip('a implementar')
    def test_regra_passaporte(self):
        boletim_raw = 'Allow citizens of Obristan'
        josef = {"passport": 'ID#: GC07D-FU8AR\nNATION: Arstotzka\nNAME: Costanza, Josef\nDOB: 1933.11.28\nSEX: M\nISS: East Grestin\nEXP: 1983.03.15'}
        inspetor = Inspetor()
        inspetor.recebe_boletim(boletim_raw)
        assert inspetor.inspeção(josef) == 'Glory to Arstotzka.'

    def test_regra_consistência_documentos(self):
        roman = {
            "passport": 'ID#: WK9XA-LKM0Q\nNATION: United Federation\nNAME: Dolanski, Roman\nDOB: 1933.01.01\nSEX: M\nISS: Shingleton\nEXP: 1983.05.12',
            "grant_of_asylum": 'NAME: Dolanski, Roman\nNATION: United Federation\nID#: Y3MNC-TPWQ2\nDOB: 1933.01.01\nHEIGHT: 176cm\nWEIGHT: 71kg\nEXP: 1983.09.20'
        }
        assert regra_consistência_documentos(
            sanitiza_papeis(roman)) == ['Detainment: ID number mismatch.']

    def test_regra_passaporte_válido(self):
        roman = {
            "passport": 'ID#: WK9XA-LKM0Q\nNATION: United Federation\nNAME: Dolanski, Roman\nDOB: 1933.01.01\nSEX: M\nISS: Shingleton\nEXP: 1983.05.12'
        }
        retorno = regra_passaporte(sanitiza_papeis(roman))
        assert not retorno

    def test_regra_passaporte_inválido(self):
        roman = {
            "passport": 'ID#: WK9XA-LKM0Q\nNATION: \nNAME: Dolanski, Roman\nDOB: 1933.01.01\nSEX: M\nISS: Shingleton\nEXP: 1983.05.12'
        }
        retorno = regra_passaporte(sanitiza_papeis(roman))
        assert 'nation' in retorno


def test_sanitiza_papeis():
    josef = {"passport": 'ID#: GC07D-FU8AR\nNATION: Arstotzka\nNAME: Costanza, Josef\nDOB: 1933.11.28\nSEX: M\nISS: East Grestin\nEXP: 1983.03.15'}
    esperado = {
        'passport': {
            'id': 'GC07D-FU8AR',
            'nation': 'Arstotzka',
            'name': 'Costanza, Josef',
            'dob': '1933.11.28',
            'sex': 'M',
            'iss': 'East Grestin',
            'exp': '1983.03.15'
        }
    }
    assert sanitiza_papeis(josef) == esperado


'''
inspector = Inspector()
bulletin = """Entrants require passport
Allow citizens of Arstotzka, Obristan"""

inspector.receive_bulletin(bulletin)

josef = {
	"passport": 'ID#: GC07D-FU8AR\nNATION: Arstotzka\nNAME: Costanza, Josef\nDOB: 1933.11.28\nSEX: M\nISS: East Grestin\nEXP: 1983.03.15'
}
guyovich = {
	"access_permit": 'NAME: Guyovich, Russian\nNATION: Obristan\nID#: TE8M1-V3N7R\nPURPOSE: TRANSIT\nDURATION: 14 DAYS\nHEIGHT: 159cm\nWEIGHT: 60kg\nEXP: 1983.07.13'
}
roman = {
	"passport": 'ID#: WK9XA-LKM0Q\nNATION: United Federation\nNAME: Dolanski, Roman\nDOB: 1933.01.01\nSEX: M\nISS: Shingleton\nEXP: 1983.05.12',
	"grant_of_asylum": 'NAME: Dolanski, Roman\nNATION: United Federation\nID#: Y3MNC-TPWQ2\nDOB: 1933.01.01\nHEIGHT: 176cm\nWEIGHT: 71kg\nEXP: 1983.09.20'
}

test.describe('Preliminary training')

test.assert_equals(inspector.inspect(josef), 'Glory to Arstotzka.');
test.assert_equals(inspector.inspect(guyovich), 'Entry denied: missing required passport.');
test.assert_equals(inspector.inspect(roman), 'Detainment: ID number mismatch.');
'''
