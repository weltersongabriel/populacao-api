from fastapi import FastAPI
from fastapi.middleware.cors import CORSMiddleware
from controllers.cidade_controller import router as cidade_router
from controllers.estado_controller import router as estado_router

app = FastAPI(title="API População Brasileira - IBGE")

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