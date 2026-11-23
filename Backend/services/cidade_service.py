import requests
import unicodedata

def _normalizar_texto(texto: str) -> str:
    """Remove acentos e converte para minúsculas para busca."""
    if not texto:
        return ""
    nfkd = unicodedata.normalize('NFKD', texto)
    return ''.join([c for c in nfkd if not unicodedata.combining(c)]).lower()

class CidadeService:
    _municipios_cache: list = []
    _cache_carregado: bool = False

    @classmethod
    def _carregar_municipios(cls) -> list:
        """Carrega e cacheia a lista de todos os municípios do IBGE."""
        if cls._cache_carregado and cls._municipios_cache:
            return cls._municipios_cache

        try:
            url = "https://servicodados.ibge.gov.br/api/v1/localidades/municipios?orderBy=nome"
            response = requests.get(url, timeout=15)
            if response.status_code == 200:
                dados = response.json()
                cls._municipios_cache = []
                for item in dados:
                    # Tenta obter UF via microrregiao -> mesorregiao -> UF
                    uf_sigla = ""
                    micro = item.get("microrregiao")
                    if micro:
                        meso = micro.get("mesorregiao")
                        if meso:
                            uf = meso.get("UF")
                            if uf:
                                uf_sigla = uf.get("sigla", "")

                    # Fallback: tenta via regiao-imediata -> regiao-intermediaria -> UF
                    if not uf_sigla:
                        regiao_imediata = item.get("regiao-imediata")
                        if regiao_imediata:
                            regiao_intermediaria = regiao_imediata.get("regiao-intermediaria")
                            if regiao_intermediaria:
                                uf = regiao_intermediaria.get("UF")
                                if uf:
                                    uf_sigla = uf.get("sigla", "")

                    cls._municipios_cache.append({
                        "codigo_ibge": str(item.get("id", "")),
                        "nome": item.get("nome", ""),
                        "uf": uf_sigla
                    })
                cls._cache_carregado = True
                return cls._municipios_cache
        except Exception as e:
            print(f"[ERRO CARREGAR MUNICÍPIOS]: {str(e)}")

        return []

    @classmethod
    def buscar_cidades_por_nome(cls, nome: str, limite: int = 20) -> dict:
        """Busca cidades pelo nome (busca parcial, case-insensitive, ignora acentos)."""
        if not nome or len(nome.strip()) < 2:
            return {"cidades": [], "total_encontrado": 0}

        municipios = cls._carregar_municipios()
        if not municipios:
            return {"error": "Falha ao carregar lista de municípios do IBGE"}

        nome_normalizado = _normalizar_texto(nome.strip())
        resultados = [
            m for m in municipios
            if nome_normalizado in _normalizar_texto(m["nome"])
        ]

        # Ordena: primeiro os que começam com o nome, depois os que contêm
        resultados.sort(key=lambda x: (
            0 if _normalizar_texto(x["nome"]).startswith(nome_normalizado) else 1,
            x["nome"]
        ))

        return {
            "cidades": resultados[:limite],
            "total_encontrado": len(resultados)
        }

    @staticmethod
    def obter_historico_e_detalhes(codigo_ibge: str) -> dict:
        """Busca histórico do Censo para uma cidade de forma segura."""
        url_antigos = f"https://servicodados.ibge.gov.br/api/v3/agregados/200/periodos/1991|2000|2010/variaveis/93?localidades=N6[{codigo_ibge}]"
        url_2022 = f"https://servicodados.ibge.gov.br/api/v3/agregados/4714/periodos/2022/variaveis/93?localidades=N6[{codigo_ibge}]"

        historico = []
        nome_cidade = ""
        uf_cidade = ""
        populacao_2022 = 0

        try:
            # 1. Consulta Censos Antigos (1991, 2000, 2010)
            res_antigos = requests.get(url_antigos, timeout=10)
            if res_antigos.status_code == 200:
                dados = res_antigos.json()
                if isinstance(dados, list) and len(dados) > 0:
                    resultados = dados[0].get('resultados', [])
                    if resultados and len(resultados) > 0:
                        series = resultados[0].get('series', [])
                        if series and len(series) > 0:
                            localidade_nome = series[0].get('localidade', {}).get('nome', '')
                            
                            # Extrai Nome e UF com segurança
                            if " - " in localidade_nome:
                                partes = localidade_nome.split(" - ")
                                nome_cidade = partes[0]
                                uf_cidade = partes[1]
                            else:
                                nome_cidade = localidade_nome

                            # Extrai os anos e valores
                            serie_anos = series[0].get('serie', {})
                            for ano, pop in serie_anos.items():
                                try:
                                    val = int(pop) if pop not in ["...", "-", None] else 0
                                except ValueError:
                                    val = 0
                                historico.append({"ano": str(ano), "populacao": val})

            # 2. Consulta Censo 2022
            res_2022 = requests.get(url_2022, timeout=10)
            if res_2022.status_code == 200:
                dados_2022 = res_2022.json()
                if isinstance(dados_2022, list) and len(dados_2022) > 0:
                    resultados_22 = dados_2022[0].get('resultados', [])
                    if resultados_22 and len(resultados_22) > 0:
                        series_22 = resultados_22[0].get('series', [])
                        if series_22 and len(series_22) > 0:
                            # Garante o nome caso a consulta antiga não tenha retornado
                            if not nome_cidade:
                                loc_nome = series_22[0].get('localidade', {}).get('nome', '')
                                if " - " in loc_nome:
                                    p = loc_nome.split(" - ")
                                    nome_cidade = p[0]
                                    uf_cidade = p[1]
                                else:
                                    nome_cidade = loc_nome

                            pop_str = series_22[0].get('serie', {}).get('2022', '0')
                            try:
                                populacao_2022 = int(pop_str) if pop_str not in ["...", "-", None] else 0
                            except ValueError:
                                populacao_2022 = 0

                            historico.append({"ano": "2022", "populacao": populacao_2022})

            # Se mesmo após tentar ambas não encontrar nome, retorna erro
            if not nome_cidade:
                return {"error": "Cidade não encontrada ou código IBGE inválido."}

            return {
                "codigo_ibge": str(codigo_ibge),
                "nome": nome_cidade,
                "uf": uf_cidade,
                "populacao_2022": populacao_2022,
                "historico": historico
            }

        except Exception as e:
            print(f"[ERRO SERVIÇO]: {str(e)}")
            return {"error": f"Erro interno ao processar requisição: {str(e)}"}

    @classmethod
    def comparar_cidades(cls, codigo_ibge_1: str, codigo_ibge_2: str) -> dict:
        """Compara os dados populacionais de duas cidades."""
        cidade1 = cls.obter_historico_e_detalhes(codigo_ibge_1)
        cidade2 = cls.obter_historico_e_detalhes(codigo_ibge_2)

        if "error" in cidade1 or "error" in cidade2:
            return {"error": "Não foi possível carregar os dados de uma ou ambas as cidades."}

        pop1 = cidade1.get("populacao_2022", 0)
        pop2 = cidade2.get("populacao_2022", 0)

        diferenca = abs(pop1 - pop2)
        mais_populosa = cidade1["nome"] if pop1 >= pop2 else cidade2["nome"]
        
        menor_pop = min(pop1, pop2)
        razao = round(max(pop1, pop2) / menor_pop, 2) if menor_pop > 0 else 0.0

        return {
            "cidade_1": cidade1,
            "cidade_2": cidade2,
            "diferenca_populacao": diferenca,
            "cidade_mais_populosa": mais_populosa,
            "razao_proporcional": razao
        }