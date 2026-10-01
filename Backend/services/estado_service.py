import requests

UF_CODIGOS = {
    "RO": "11", "AC": "12", "AM": "13", "RR": "14", "PA": "15", "AP": "16", "TO": "17",
    "MA": "21", "PI": "22", "CE": "23", "RN": "24", "PB": "25", "PE": "26", "AL": "27",
    "SE": "28", "BA": "29", "MG": "31", "ES": "32", "RJ": "33", "SP": "35", "PR": "41",
    "SC": "42", "RS": "43", "MS": "50", "MT": "51", "GO": "52", "DF": "53"
}

class EstadoService:
    @staticmethod
    def obter_top10_cidades(uf: str) -> dict:
        uf_upper = uf.upper()
        codigo_uf = UF_CODIGOS.get(uf_upper)

        if not codigo_uf:
            return {"error": f"UF '{uf}' inválida ou não encontrada."}

        url = f"https://servicodados.ibge.gov.br/api/v3/agregados/4714/periodos/2022/variaveis/93?localidades=N6[N3[{codigo_uf}]]"

        try:
            response = requests.get(url, timeout=10)
            if response.status_code != 200:
                return {"error": "Falha na comunicação com a API do IBGE"}

            dados = response.json()
            cidades_formatadas = []

            if dados and len(dados) > 0:
                series = dados[0].get("resultados", [])[0].get("series", [])
                
                for item in series:
                    nome_completo = item.get("localidade", {}).get("nome", "")
                    codigo_ibge = item.get("localidade", {}).get("id", "")
                    populacao_str = item.get("serie", {}).get("2022", "0")

                    try:
                        populacao = int(populacao_str)
                    except ValueError:
                        populacao = 0

                    cidades_formatadas.append({
                        "codigo_ibge": codigo_ibge,
                        "nome": nome_completo,
                        "uf": uf_upper,
                        "populacao": populacao
                    })

            
            cidades_ordenadas = sorted(
                cidades_formatadas, 
                key=lambda x: x["populacao"], 
                reverse=True
            )

            
            top10 = cidades_ordenadas[:10]

            return {
                "uf": uf_upper,
                "total_encontrado": len(top10),
                "cidades": top10
            }

        except Exception as e:
            return {"error": f"Erro interno ao processar dados: {str(e)}"}