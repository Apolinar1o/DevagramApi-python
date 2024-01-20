from datetime import datetime
import os

from fastapi import APIRouter, Body, HTTPException, Depends, Header, UploadFile

from middleware.JwtMiddleWare import verificar_token
from models.usuarioModel import UsuarioModel, UsuarioCriarModel
from services.AuthService import decodificar_token_jwt
from services.UsuarioServices import (registrar_usuario, buscar_usuario)
from services.AuthService import decodificar_token_jwt




router = APIRouter()

@router.post("/", response_description="Rota para criar um novo usuário")
async def rota_criar_usuario(file: UploadFile,  usuario: UsuarioCriarModel = Depends(UsuarioCriarModel)):
    try:
        caminho_arquivo = f"files/foto-{datetime.now(). strftime("%H%M%S")}.png"

        with open(caminho_arquivo, "wb+") as arquivo:
            arquivo.write(file.file.read())
        resultado = await registrar_usuario(usuario, caminho_arquivo)

        os.remove(caminho_arquivo)


        if not resultado["status"] == 201:
                raise HTTPException(status_code=resultado['status'], detail=resultado['mensagem'])

        return resultado
    except Exception as erro:
        raise erro


@router.get(
    "/me",
    response_description="Rota para buscar informações do usuario logado",
    dependencies=[Depends(verificar_token)]
)
async def buscar_info_usuario_logado(Authorization: str = Header(default="")):
    try:
        token = Authorization.split(" ")[1]

        payload = decodificar_token_jwt(token)

        resultado = await buscar_usuario(payload["usuario_id"])
        if not resultado["status"] == 200:
            raise HTTPException(status_code=resultado['status'], detail=resultado)
        return resultado

    except Exception as error:
        raise error
