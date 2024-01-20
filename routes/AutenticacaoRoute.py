from fastapi import APIRouter, Body, HTTPException
from models.usuarioModel import  UsuarioLoginModel
from services.AuthService import login_service, gerar_token_jwt
from services.UsuarioServices import UsuarioService

router = APIRouter()
usuarioService = UsuarioService()
print("usuarioService")
@router.post("/login")
async def login(usuario: UsuarioLoginModel = Body((...))):
    print("11111111111111111111111111")
    resultado = await login_service(usuario)


    if not resultado['status'] == 200:
        raise HTTPException(status_code=resultado['status'], detail=resultado['mensagem'])


    del resultado["dados"]["senha"]
    token = gerar_token_jwt(resultado["dados"]["id"])
    resultado["dados"]["token"] = token
    return resultado
