from pydantic import BaseModel
from typing import List

class HistoricoAno(BaseModel):
    ano: str
    populacao: int

class CidadeDetalheResponse(BaseModel):
    codigo_ibge: str
    nome: str
    uf: str
    populacao_2022: int
    historico: List[HistoricoAno]

class ComparacaoCidadesResponse(BaseModel):
    cidade_1: CidadeDetalheResponse
    cidade_2: CidadeDetalheResponse
    diferenca_populacao: int
    cidade_mais_populosa: str
    razao_proporcional: float