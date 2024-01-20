
from fastapi import FastAPI, Body
from routes.UsuarioRoute import router as UsuarioRoute
from routes.AutenticacaoRoute import router as AutenticacaoRoute
app = FastAPI()
app.include_router(UsuarioRoute, tags=["Usuario"], prefix="/api/usuario")
app.include_router(AutenticacaoRoute, tags=["autenticacao"], prefix="/api/auth")
@app.get("/", tags=["Health"])
async def heath():
    return {
        "status": "OK!"
    }
