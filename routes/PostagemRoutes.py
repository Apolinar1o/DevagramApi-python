from datetime import datetime
import os

from fastapi import APIRouter, HTTPException, Depends, Header, UploadFile

from middleware.JwtMiddleWare import verificar_token
from models.PostagemModel import PostagemCriarModel

router = APIRouter()

@router.post("/", response_description="Rota para criar um novo post")
async def rota_criar_postagem(file: UploadFile,  usuario: PostagemCriarModel = Depends(PostagemCriarModel)):
    try:
        caminho_arquivo = f"files/foto-{datetime.now(). strftime("%H%M%S")}.png"

        with open(caminho_arquivo, "wb+") as arquivo:
            arquivo.write(file.file.read())
        #resultado = await registrar_usuario(usuario, caminho_arquivo)

        os.remove(caminho_arquivo)

    except Exception as erro:
        raise erro


@router.get(
    "/",
    response_description="Rota para buscar postagens do usuario logado",
    dependencies=[Depends(verificar_token)]
)
async def buscar_info_usuario_logado(Authorization: str = Header(default="")):
    try:

        return {
            "teste": "Ok"
        }


    except:
        raise HTTPException(status_code=500['status'], detail='Erro interno no servidor')
