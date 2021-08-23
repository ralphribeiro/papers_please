from abc import ABC, abstractmethod
from dataclasses import dataclass, field
from datetime import date
import re
from typing import Iterable, Optional

 
@dataclass
class Regra(ABC):
    @abstractmethod
    def executar(self, papel) -> str:
        """ Deve ser implementado """


class RegraNativo(Regra):
    def executar(self, papel) -> str:
        return super().executar(papel)


class RegraIdCard(Regra):
    def executar(self, papel) -> str:
        return super().executar(papel)


class RegraVacinas(Regra):
    ...


class RegraGarantiaAsilo(Regra):
    ...


class RegraPermissãoTrabalho(Regra):
    ...


class RegraAutorizaçãoAutomática(Regra):
    ...


@dataclass
class Boletim:
    descrição: str
    dt: Optional[date] = field(default_factory=date.today)
    lista_nações = [
        'Arstotzka', 'Antegria', 'Impor', 'Kolechia',
        'Obristan', 'Republia', 'United Federation'
    ]

    nacões: dict = field(init=False)
    documentos: dict = field(init=False)
    # vacinas: dict = field(init=False)
    # procurado: list[str] = field(init=False)

    def _encontra_padrões(self, pat1: Iterable, pat2: Iterable) -> dict:
        ret = {}
        for t in self.descrição.split('\n'):
            p = re.compile('|'.join(pat for pat in pat1))
            encontrado = p.search(t)
            if encontrado:
                p2 = re.compile('|'.join(pat for pat in pat2))
                encontrado2 = p2.finditer(t)
                if encontrado2:
                    ret[encontrado.group()] = tuple(r.group()
                                                    for r in encontrado2)
        return ret

    def __post_init__(self):
        self.nacões = self._encontra_padrões(
            ('Allow', 'Deny', ),
            self.lista_nações
        )

        self.documentos = self._encontra_padrões(
            ('Foreigners', 'Citizens', 'Workers', ),
            ('require', 'pass', 'access', 'permit', 'work', 'ID card', )
        )

        # self.vacinas =
        # self.procurado =


def regra_consistência_documentos(papeis: dict[str, dict]) -> list:
    papeis_ = {}
    retorno = []
    for papel, valor in papeis.items():
        for k, v in valor.items():
            if k == 'exp':
                continue
            if k in papeis_ and papeis_[k][0] != v:
                if k == 'id':
                    retorno.append('Detainment: ID number mismatch.')
                else:
                    retorno.append(f'Detainment: {k} mismatch.')
            papeis_[k] = v, papel
    return retorno


def regra_passaporte(papeis) -> list:
    return [k for k, v in papeis['passport'].items() if not v]


def regra_permissão_acesso(papeis) -> list:
    return [k for k, v in papeis['access_permit'].items() if not v]


def regra_validade_documento(papeis) -> list:
    return []


def sanitiza_papeis(entrante: dict) -> dict:
    papeis = {}
    for ch, vl in entrante.items():
        linhas = vl.splitlines()
        atributos = {}
        for li in linhas:
            chave, valor = li.split(':')
            if '#' in chave:
                chave = chave.removesuffix('#')
            atributos[chave.lower()] = valor.strip()
        papeis[ch] = atributos
    return papeis


class Inspetor:
    def __init__(self) -> None:
        self.boletins: list[Boletim] = []

    def recebe_boletim(self, boletim_raw: str) -> None:
        self.boletins.append(Boletim(boletim_raw))

    def inspeção(self, entrante: dict) -> str:
        boletim = next((b for b in (self.boletins)), None)

        papeis = {k: sanitiza_papeis(v) for k, v in entrante.items()}
