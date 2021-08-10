from dataclasses import dataclass, field
from datetime import date
from typing import Callable


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
        self.nome = ch
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
