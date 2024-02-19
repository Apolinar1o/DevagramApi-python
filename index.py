print("111111111111111111111111111")
from fastapi import FastAPI, Body
from fastapi.middleware.cors import CORSMiddleware
from routes.UsuarioRoute import router as UsuarioRoute
from routes.AutenticacaoRoute import router as AutenticacaoRoute
from routes.PostagemRoutes import router as PostagemRoute

origins = [
    "*"
]

app = FastAPI()


app.include_router(UsuarioRoute, tags=["Usuario"], prefix="/api/usuario")
app.include_router(AutenticacaoRoute, tags=["autenticacao"], prefix="/api/auth")
app.include_router(PostagemRoute, tags=["postagem"], prefix="/api")
app.add_middleware(
    CORSMiddleware,
    allow_origins=origins,
    allow_credentials=True,
    allow_methods=["*"],
    allow_headers =["*"],

)



@app.get("/", tags=["Health"])
async def heath():
    return {
        "status": "OK!"
    }