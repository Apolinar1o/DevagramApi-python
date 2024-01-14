from fastapi import APIRouter, Body, HTTPException

from models.usuarioModel import  UsuarioLoginModel
from services.AuthService import login_service
from services.UsuarioServices import registrar_usuario

router = APIRouter()
print("111111111")
@router.post("/login")
async def login(usuario: UsuarioLoginModel = Body((...))):
    resultado = await login_service(usuario)
   
    if not resultado["status"] == 201:
        raise HTTPException(status_code=resultado['status'], detail=resultado['mensagem'])
    return resultado