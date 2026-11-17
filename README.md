<div align="center">

# 🌎 Sistema Populacional IBGE — **Backend API**

### API REST para consulta, evolução e comparação de dados demográficos dos municípios brasileiros — com foco na **Bahia**

<p>
  <img src="https://img.shields.io/badge/Python-3.10+-3776AB?style=for-the-badge&logo=python&logoColor=white" alt="Python" />
  <img src="https://img.shields.io/badge/FastAPI-0.100+-009688?style=for-the-badge&logo=fastapi&logoColor=white" alt="FastAPI" />
  <img src="https://img.shields.io/badge/IBGE-API%20Oficial-2E7D32?style=for-the-badge" alt="IBGE API" />
  <img src="https://img.shields.io/badge/Status-Em%20desenvolvimento-F59E0B?style=for-the-badge" alt="Status" />
</p>

<p>
  <a href="#-sobre-o-projeto">Sobre</a> •
  <a href="#-funcionalidades-da-api">Funcionalidades</a> •
  <a href="#-arquitetura">Arquitetura</a> •
  <a href="#-tecnologias">Tecnologias</a> •
  <a href="#-como-executar">Como executar</a> •
  <a href="#-endpoints">Endpoints</a> •
  <a href="#-equipe">Equipe</a>
</p>

</div>

---

## 📖 Sobre o projeto

O **Sistema Populacional IBGE - Backend** é uma **API REST** desenvolvida em Python com FastAPI que consome as APIs públicas do **IBGE (Instituto Brasileiro de Geografia e Estatística)** para transformar dados do Censo em informação estruturada e pronta para consumo por frontends.

> ⚠️ **IMPORTANTE:** Este repositório contém **apenas o backend** da aplicação. O frontend (React) foi desenvolvido separadamente e não faz parte deste repositório.

> 🎓 **Projeto acadêmico** desenvolvido para a unidade curricular **Sistemas Distribuídos e Mobile**.

---

## ✨ Funcionalidades da API

| Recurso | Descrição |
| :--- | :--- |
| 🏆 **Top 10 municípios** | Ranking das cidades mais populosas da Bahia (rota padrão) e suporte aos demais estados. |
| 📈 **Evolução do Censo** | Série histórica do crescimento populacional de 1991 a 2022 para qualquer município do Brasil. |
| ⚖️ **Comparador demográfico** | Compara duas cidades, retornando diferença absoluta e razão de proporção entre elas. |
| 📚 **Documentação automática** | Swagger UI e ReDoc disponíveis em `/docs` e `/redoc`. |

---

## 🏗️ Arquitetura

A API atua como camada intermediária: consulta o IBGE, trata/normaliza os dados e entrega via JSON para o frontend consumir.

```mermaid
flowchart LR
    FE[⚛️ Frontend<br/>(React - repo separado)] -->|HTTP / JSON| BE[🐍 Backend API<br/>FastAPI]
    BE -->|Requisições| IBGE[(🏛️ APIs do IBGE)]
    IBGE -->|Dados do Censo| BE
    BE -->|Dados tratados| FE
```

### 📁 Estrutura de pastas

```text
populacao-api/
└── Backend/                    # API REST em Python com FastAPI
    ├── main.py                 # Ponto de entrada da aplicação e configuração de CORS
    ├── controllers/            # Endpoints HTTP da API
    ├── services/               # Regras de negócio e integração com o IBGE
    ├── schemas/                # Validação de tipos com Pydantic
    ├── models/                 # Modelos internos de domínio
    ├── utils/                  # Utilitários e helpers
    └── requirements.txt        # Dependências Python
```

---

## 🛠️ Tecnologias

**Backend**
- [Python 3.10+](https://www.python.org/)
- [FastAPI](https://fastapi.tiangolo.com/) — framework da API REST
- [Pydantic](https://docs.pydantic.dev/) — validação e serialização de dados
- [Uvicorn](https://www.uvicorn.org/) — servidor ASGI

**Fonte de dados**
- [APIs de Dados do IBGE](https://servicodados.ibge.gov.br/api/docs) — Censo Demográfico

---

## 🚀 Como executar

### 📋 Pré-requisitos

- [Python 3.10+](https://www.python.org/downloads/)
- [Git](https://git-scm.com/)

### 1️⃣ Clonar o repositório

```bash
git clone <URL_DO_REPOSITORIO_NO_GITHUB>
cd populacao-api
```

### 2️⃣ Configurar e rodar o Backend

```bash
cd Backend

# Crie e ative um ambiente virtual
python -m venv venv

# Linux / macOS
source venv/bin/activate
# Windows
venv\Scripts\activate

# Instale as dependências
pip install -r requirements.txt

# Inicie o servidor
uvicorn main:app --reload
```

✅ API disponível em **http://localhost:8000**  
📚 Documentação interativa (Swagger) em **http://localhost:8000/docs**  
📖 Documentação alternativa (ReDoc) em **http://localhost:8000/redoc**

---

## 🔗 Endpoints

| Método | Endpoint | Descrição |
| :--- | :--- | :--- |
| `GET` | `/` | Retorna o Top 10 municípios da Bahia (rota padrão) |
| `GET` | `/municipios/top10` | Top 10 municípios por estado (query param: `uf`) |
| `GET` | `/municipios/{codigo_ibge}/evolucao` | Evolução populacional 1991-2022 |
| `GET` | `/municipios/comparar` | Compara dois municípios (query params: `cod1`, `cod2`) |

> 💡 Acesse **http://localhost:8000/docs** para testar os endpoints interativamente.

---

## 👥 Nossa Equipe

### Os desenvolvedores por trás do projeto

<br/>
<table>
  <tr>
    <td align="center" width="200">
      <img src="https://avatars.githubusercontent.com/u/179327949?v=4" width="120" alt="Welterson Gabriel" /><br/><br/>
      <h3>Welterson<br/>Gabriel</h3>
      <sub></sub>
    </td>
    <td align="center" width="200">
      <img src="https://avatars.githubusercontent.com/u/102553070?v=4" width="120" alt="Guilherme Silva" /><br/><br/>
      <h3>Guilherme<br/>Silva</h3>
      <sub></sub>
    </td>
    <td align="center" width="200">
      <img src="https://avatars.githubusercontent.com/u/242506933?v=4" width="120" alt="Eric Junqueira" /><br/><br/>
      <h3>Eric<br/>Junqueira</h3>
      <sub></sub>
    </td>
    <td align="center" width="200">
      <img src="https://avatars.githubusercontent.com/u/203365599?v=4" width="120" alt="Gustavo Gomes" /><br/><br/>
      <h3>Gustavo<br/>Gomes</h3>
      <sub></sub>
    </td>
    <td align="center" width="200">
      <img src="https://avatars.githubusercontent.com/u/169108489?v=4" width="120" alt="Gabriel Fernando" /><br/><br/>
      <h3>Gabriel<br/>Fernando</h3>
      <sub></sub>
    </td>
  </tr>
</table>
<br/>

---

## 🎓 Orientação Acadêmica

<img src="https://img.shields.io/badge/Unidade%20Curricular-Sistemas%20Distribu%C3%ADdos%20e%20Mobile-1D4ED8?style=for-the-badge&logo=bookstack&logoColor=white" alt="Unidade Curricular" />
<br/><br/>

<img src="https://img.shields.io/badge/Professor%20Orientador-Joilson%20Amorim%20Moreira-0F766E?style=for-the-badge&logo=googleclassroom&logoColor=white" alt="Professor Orientador" />
<br/><br/>

> 👨‍🏫 *Agradecemos ao professor **Joilson Amorim Moreira** pela orientação e apoio durante todo o desenvolvimento deste projeto.*

---

## 📄 Licença

Este projeto foi desenvolvido para fins acadêmicos. Os dados utilizados pertencem ao **IBGE** e são de acesso público.

<div align="center">

Dados: [IBGE](https://www.ibge.gov.br/)

</div>