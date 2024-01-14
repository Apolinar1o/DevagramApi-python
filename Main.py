
from fastapi import FastAPI, Body
from routes.UsuarioRoute import router as UsuarioRoute
from routes.AutenticacaoRoute import router as AutenticacaoRoute
print("22222222222222222222222")
app = FastAPI()
app.include_router(UsuarioRoute, tags=["Usuario"], prefix="/api/usuario")
print("33333333333333333333333")
app.include_router(AutenticacaoRoute, tags=["autenticacao"], prefix="/api/auth")


@app.get("/", tags=["Health"])
async def heath():
    return {
        "status": "OK!"
    }