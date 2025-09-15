from dataclasses import dataclass, asdict
from datetime import datetime
import uuid
from typing import List

def new_id():
    return str(uuid.uuid4())

@dataclass
class Jogadora:
    id: str
    nome: str
    idade: int
    contato: str
    ativa: bool = True
    created_at: str = datetime.utcnow().isoformat()

    def to_dict(self):
        return asdict(self)

@dataclass
class Documento:
    id: str
    jogadora_id: str
    filename: str
    filetype: str
    status: str  # pending | approved | rejected
    uploaded_at: str = datetime.utcnow().isoformat()
    history: List[dict] = None

    def to_dict(self):
        d = asdict(self)
        if self.history is None:
            d['history'] = []
        return d

@dataclass
class Time:
    id: str
    nome: str
    integrantes: List[str]
    created_at: str = datetime.utcnow().isoformat()

    def to_dict(self):
        return asdict(self)

@dataclass
class Torneio:
    id: str
    nome: str
    vagas: int
    inscritos: List[str]
    created_at: str = datetime.utcnow().isoformat()

    def to_dict(self):
        return asdict(self)

@dataclass
class Inscricao:
    id: str
    torneio_id: str
    time_id: str
    status: str  # confirmed | waiting | canceled
    created_at: str = datetime.utcnow().isoformat()

    def to_dict(self):
        return asdict(self)