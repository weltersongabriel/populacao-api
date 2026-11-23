import os
from contextlib import asynccontextmanager
from fastapi import FastAPI
from fastapi.middleware.cors import CORSMiddleware
from controllers.cidade_controller import router as cidade_router
from controllers.estado_controller import router as estado_router
from services.cidade_service import CidadeService

# Pre-carrega cache de municípios na inicialização para evitar timeout na primeira busca
@asynccontextmanager
async def lifespan(app: FastAPI):
    # Startup
    print("[STARTUP] Pré-carregando cache de municípios...")
    try:
        municipios = CidadeService._carregar_municipios()
        print(f"[STARTUP] Cache carregado: {len(municipios)} municípios")
    except Exception as e:
        print(f"[STARTUP] Aviso: falha ao pré-carregar cache: {e}")
    yield
    # Shutdown (opcional)
    print("[SHUTDOWN] Encerrando aplicação...")

app = FastAPI(
    title="API População Brasileira - IBGE",
    lifespan=lifespan
)

# Habilita o CORS para o Frontend React acessar
app.add_middleware(
    CORSMiddleware,
    allow_origins=["*"],
    allow_credentials=True,
    allow_methods=["*"],
    allow_headers=["*"],
)

# Registra os controllers
app.include_router(cidade_router)
app.include_router(estado_router)


@app.get("/")
def home():
    return {"status": "Backend operacional"}


@app.get("/health")
def health_check():
    """Health check para Railway/Load Balancer."""
    return {"status": "healthy"}


@app.get("/health/detailed")
def health_detailed():
    """Health check detalhado com status do cache."""
    cache_status = "loaded" if CidadeService._cache_carregado else "not_loaded"
    cache_count = len(CidadeService._municipios_cache) if CidadeService._municipios_cache else 0
    return {
        "status": "healthy",
        "cache": {
            "status": cache_status,
            "municipios_carregados": cache_count
        }
    }