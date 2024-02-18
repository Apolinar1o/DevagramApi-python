from datetime import datetime
import os

from fastapi import APIRouter, Body, HTTPException, Depends, Header, UploadFile

from middleware.JwtMiddleWare import verificar_token
from models.usuarioModel import UsuarioModel, UsuarioCriarModel, UsuarioAtualizarModel
from services.UsuarioServices import UsuarioService
from services.AuthService import AuthService

router = APIRouter()
usuarioService = UsuarioService()
authService = AuthService()
@router.post("/", response_description="Rota para criar um novo usuário")
async def rota_criar_usuario(file: UploadFile,  usuario: UsuarioCriarModel = Depends(UsuarioCriarModel)):
    try:
        caminho_arquivo = f"files/foto-{datetime.now(). strftime("%H%M%S")}.png"

        with open(caminho_arquivo, "wb+") as arquivo:
            arquivo.write(file.file.read())
        resultado = await usuarioService.registrar_usuario(usuario, caminho_arquivo)
        os.remove(caminho_arquivo)
        if not resultado["status"] == 201:
            raise HTTPException(status_code=resultado["status"], detail=resultado["mensagem"])
        print("----------------------")
        return resultado.__dict__
    except Exception as erro:
        raise erro


@router.get(
    "/me",
    response_description="Rota para buscar informações do usuario logado",
    dependencies=[Depends(verificar_token)]
)
async def buscar_info_usuario_logado(Authorization: str = Header(default=""), ):

    try:

        resultado = await authService.validar_usuario_logado(Authorization)

        if not resultado.status == 200:
            raise HTTPException(status_code=resultado.status, detail=resultado.mensagem)
        return resultado.__dict__

    except Exception as error:
        raise error

@router.get(
    "/{usuario_id}",
    response_description="Rota para buscar informações do usuario logado",
    dependencies=[Depends(verificar_token)]
)
async def buscar_info_usuario_logado(usuario_id: str):
    try:
        resultado = await usuarioService.buscar_usuario(usuario_id)
        if not resultado.status == 200:
            raise HTTPException(status_code=resultado.status, detail=resultado.mensagem)
        return resultado.__dict__

    except Exception as error:
        raise error




@router.put(
    "/me",
    response_description="Rota para atualizar informações do usuario logado",
    dependencies=[Depends(verificar_token)]
)
async def atualizar_usuario_logado(Authorization: str = Header(default=""), usuario: UsuarioAtualizarModel = Depends(UsuarioAtualizarModel)):
    try:
        resultado = await authService.validar_usuario_logado(Authorization)
        if not resultado.status == 200:
            raise HTTPException(status_code=resultado.status, detail=resultado.mensagem)
        return resultado.__dict__

    except Exception as error:
        raise error

@router.put(
    "/seguir/{usuario_id}",
    response_description="Rota para follow/unfollow em um usuário",
    dependencies=[Depends(verificar_token)]
)
async def seguir_deseguir(usuario_id, Authorization: str = Header(default="")):
    try:
        resultado = await authService.validar_usuario_logado(Authorization)
        user = resultado.dados["id"]



        seguir = await usuarioService.seguir_usuario(user, usuario_id)

        if not seguir.status == 201:
            raise HTTPException(status_code=seguir.status, detail=seguir.mensagem)
        return seguir.__dict__


    except Exception as error:
        print(error)
        raise error

@router.get(
    "/",
    response_description="Rota para listar todos os usuarios",
    dependencies=[Depends(verificar_token)]
)
async def buscar_info_usuario_logado(nome: str):
    try:

        resultado = await usuarioService.listar_usuarios(nome)

        if not resultado.status == 200:
            raise HTTPException(status_code=resultado.status, detail=resultado.mensagem)
        return resultado.__dict__

    except Exception as error:
        raise error