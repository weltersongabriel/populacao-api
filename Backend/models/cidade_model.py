class Cidade:
    def __init__(self, codigo_ibge: str, nome: str, uf: str, populacao: int = 0):
        self.codigo_ibge = codigo_ibge
        self.nome = nome
        self.uf = uf
        self.populacao = populacao