import requests

class IBGEService:
    @staticmethod
    def obter_historico_cidade(codigo_ibge: str) -> dict:

        url = f"https://servicodados.ibge.gov.br/api/v1/projecoes/populacao/{codigo_ibge}"
        response = requests.get(url)
    
        if response.status_code != 200:
            return {"codigo_ibge": codigo_ibge, "nome": "Desconhecido", "historico": []}

        data = response.json()

        historico_formatado = []
        if data and len(data) > 0:
            nome_cidade = data[0]['resultados'][0]['series'][0]['localidade']['nome']
            series = data[0]['resultados'][0]['series'][0]['serie']

            for ano, valor in series.items():
                historico_formatado.append({
                    "ano": int(ano), "populacao": int(valor) if valor != "..."else 0})

            else:
                nome_cidade = "Cidade não encontrada"

        return {
            "codigo_ibge": codigo_ibge,
            "nome": nome_cidade,
            "historico": historico_formatado   
        }