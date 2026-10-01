from pydantic import BaseModel
from typing import List

class CidadeTop10(BaseModel):
    codigo_ibge: str
    nome: str
    uf: str
    populacao: int

class Top10EstadoResponse(BaseModel):
    uf: str
    total_encontrado: int
    cidades: List[CidadeTop10]