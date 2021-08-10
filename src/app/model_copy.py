from dataclasses import dataclass, field


@dataclass
class Papel:
    raw: dict
    nome: str = field(init=False, default_factory=str)
    items: dict = field(init=False, default_factory=dict)

    def _sanitiza(self):
        ch, vl = self.raw.values()
        atributos = {}
        for li in vl:
            chave, valor = li.split(':')
            if '#' in chave:
                chave = chave.removesuffix('#')
            atributos[chave.lower()] = valor.strip()
        # self.nome = ch
        self.items = atributos

    def __post_init__(self):
        self._sanitiza()


class Regra:
    ...


class Entrante:
    def __init__(self, papeis: list[Papel], regras: list[Regra]) -> None:
        self.papeis = papeis
