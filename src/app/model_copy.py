from dataclasses import dataclass, field
from datetime import date
import re
from typing import Callable, Iterable


@dataclass
class Boletim:
    raw: str
    nações_permitidas: tuple = field(init=False)
    vacinação: tuple = field(init=False)

    _NAÇÕES: tuple = field(init=False, default=(
        'Arstotzka', 'Antegria', 'Impor', 'Kolechia',
        'Obristan', 'Republia', 'United Federation'
    ))

    @staticmethod
    def encontra_padrões(
        alvo: str, padrão1: Iterable, padrão2: Iterable
    ) -> tuple:
        ret = ()
        for t in alvo.split('\n'):
            p = re.compile('|'.join(pat for pat in padrão1))
            encontrado = p.search(t)
            if encontrado:
                p2 = re.compile('|'.join(pat for pat in padrão2))
                encontrado2 = p2.finditer(t)
                if encontrado2:
                    ret = tuple(r.group() for r in encontrado2)
        return ret

    def _nações(self):
        p1 = ('Allow', )
        self.nações_permitidas = self.encontra_padrões(
            self.raw, p1, self._NAÇÕES)

    def _vacinação(self):
        p1 = ('vaccination', )
        self._vacinação = self.encontra_padrões(
            self.raw, p1, 
        )

    def __post_init__(self):
        self._nações()


@dataclass
class Papel:
    raw: dict
    nome: str = field(init=False, default_factory=str)
    itens: dict = field(init=False, default_factory=dict)

    def _sanitiza(self):
        ch, vl = self.raw.popitem()
        atributos = {}
        for li in vl.splitlines():
            chave, valor = li.split(':')
            if '#' in chave:
                chave = chave.removesuffix('#')
            atributos[chave.lower()] = valor.strip()
        self.nome = ch.lower()
        self.itens = atributos

    def __post_init__(self):
        self._sanitiza()


class Entrante:
    def __init__(
        self, papeis: dict, regras: list[Callable]
    ) -> None:
        self.papeis: list[Papel] = self.constroi_papeis(papeis)
        self.regras = list(regras)
        self.status = []

    @staticmethod
    def constroi_papeis(papeis: dict) -> list[Papel]:
        return [Papel({k: v}) for k, v in papeis.items()]

    def submete_papeis_regras(self):
        return [fn(self) for fn in self.regras]


def regra_consistência_documentos(entrante: Entrante):
    papeis_ = {}
    for papel in entrante.papeis:
        for k, v in papel.itens.items():
            if k == 'exp':
                continue
            if k in papeis_ and papeis_[k][0] != v:
                if k == 'id':
                    entrante.status.append('Detainment: ID number mismatch.')
                else:
                    entrante.status.append(f'Detainment: {k} mismatch.')
            papeis_[k] = v, papel.nome


def regra_valida_data(entrante: Entrante):
    for papel in entrante.papeis:
        a, m, d = (int(p) for p in papel.itens['exp'].split('.'))
        validade_papel = date(year=a, month=m, day=d)
        validade = date.fromisoformat('1982-11-22')
        if validade_papel < validade:
            entrante.status.append(f'Entry denied: {papel.nome} expired.')


def regra_passaporte_obrigatório(entrante: Entrante):
    if 'passport' not in [p.nome for p in entrante.papeis]:
        entrante.status.append('Entry denied: missing required passport.')


def regra_id_card_obrigatório(entrante: Entrante):
    if 'id_card' not in [p.nome for p in entrante.papeis]:
        entrante.status.append('Entry denied: missing required ID card.')


def regra_vacinação_obrigatória(vacinas_exigidas: dict, entrante: Entrante):
    nação = ''
    vacinas_tomadas = ''
    for p in entrante.papeis:
        if p.nome == 'passport':
            nação = p.itens['nation']
        if p.nome == 'certificate_of_vaccination':
            vacinas_tomadas = p.itens['vaccines']

    for v in vacinas_exigidas[nação]:
        if v not in vacinas_tomadas:
            s = 'Entry denied: missing required {} vaccination.'
            entrante.status.append(s.format(v))


def regra_nações_permitidas(nações_permitidas: dict, entrante: Entrante):
    nação = [
        p.itens['nation'] for p in entrante.papeis if p.nome == 'passport'
    ].pop()

    if nação not in nações_permitidas['allow']:
        s = 'Entry denied: Entrant from {}.'
        entrante.status.append(s.format(nação))


def regra_criminal(procurados: tuple, entrante: Entrante):
    nome = [
        p.itens['name'] for p in entrante.papeis if p.nome == 'passport'
    ].pop()
    if nome in procurados:
        entrante.status.append('Detainment: Entrant is a wanted criminal.')


def regra_permissão_acesso(entrante: Entrante):
    if 'access_permit' not in [p.nome for p in entrante.papeis]:
        entrante.status.append('Entry denied: missing required access permit.')


def regra_visto_trabalho(entrante: Entrante):
    if 'work_pass' not in [p.nome for p in entrante.papeis]:
        entrante.status.append('Entry denied: Workers require work pass.')


def regra_autorização_diplomática(entrante: Entrante):
    if 'diplomatic_authorization' not in [p.nome for p in entrante.papeis]:
        entrante.status.append(
            'Entry denied: invalid diplomatic authorization.'
        )
