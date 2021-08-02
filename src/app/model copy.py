from dataclasses import dataclass, field
from datetime import datetime
from typing import Callable


@dataclass
class Passaporte:
    identificador: str
    validade: datetime


@dataclass
class CarteiraVacinação:
    vacinas: list[str] = field(default_factory=list)


@dataclass
class Cidadão:
    nome: str
    nacionalidade: str

    passaporte: Passaporte
    carteira_vacinação: CarteiraVacinação

    id_card: str


@dataclass
class Boletim:
    descrição: str
    data: datetime


@dataclass(init=False)
class Inspetor:
    boletins: list[Boletim] = field(default_factory=list)
    regras: list[Callable] = field(default_factory=list)
