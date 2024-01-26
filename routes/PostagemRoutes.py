from datetime import datetime
import os
from fastapi import APIRouter, HTTPException, Depends, Header, UploadFile, Body
from middleware.JwtMiddleWare import verificar_token
from models.ComentariosModel import ComentarioModel, ComentarioCriarModel
from models.PostagemModel import PostagemCriarModel
from services.AuthService import AuthService
from services.UsuarioServices import UsuarioService
from services.PostagemService import PostagemService


router = APIRouter()
authService = AuthService()
usuarioService = UsuarioService()
postagemService = PostagemService()


@router.post("/postagem", response_description="Rota para criar um novo post", dependencies=[Depends(verificar_token)])
async def rota_criar_postagem(postagem: PostagemCriarModel = Depends(PostagemCriarModel), Authorization: str = Header(default="")):
    try:
        token = Authorization.split(" ")[1]
        payload = authService.decodificar_token_jwt(token)

        resultado = await(usuarioService.buscar_usuario(payload["usuario_id"]))

        usuario_logado = resultado["dados"]

        resultado = await postagemService.cadastrar_postagem(postagem, usuario_logado["id"])
        if not resultado["status"] == 201:
            raise HTTPException(status_code=resultado["status"], detail=resultado["mensagem"])

        return resultado
    except Exception as erro:
        raise erro


@router.get(
    "/postagem",
    response_description="Rota para buscar postagens do usuario logado",
    dependencies=[Depends(verificar_token)]
)
async def buscar_info_usuario_logado():
    try:
        resultado = await postagemService.listar_postagens()

        if not resultado["status"] == 200:
            raise HTTPException(status_code=resultado["status"], detail=resultado["mensagem"])
        return resultado
    except:
        raise HTTPException(status_code=500, detail='Erro interno no servidor')

@router.put(
    "/postagem/curtir",
    response_description="Rota para curtir e descurtir",
    dependencies=[Depends(verificar_token)]
)
async def curtir_descurtir(postagem, Authorization: str = Header(default="")):
    try:

        token = Authorization.split(" ")[1]
        payload = authService.decodificar_token_jwt(token)
        resultado = await (usuarioService.buscar_usuario(payload["usuario_id"]))

        user = resultado["dados"]["id"]

        comentario = await postagemService.curtir_descurtir(postagem, user)
        if not comentario["status"] == 201:
            raise HTTPException(status_code=resultado["status"], detail=resultado["mensagem"])
        return comentario

    except Exception as error:
        print(error)
        raise error

@router.put(
    "/postagem/comentar",
    response_description="Rota para criar um comentario em uma postagem",
    dependencies=[Depends(verificar_token)]
)
async def comentar_postagem(postagem, comentario = Body(...) ,Authorization: str = Header(default="")):
    try:
        token = Authorization.split(" ")[1]
        payload = authService.decodificar_token_jwt(token)
        resultado = await (usuarioService.buscar_usuario(payload["usuario_id"]))

        user = resultado["dados"]["id"]

        comentario = await postagemService.criar_comentario(postagem, user, comentario)
        if not comentario["status"] == 201:
            raise HTTPException(status_code=resultado["status"], detail=resultado["mensagem"])
        return comentario

    except Exception as error:
        print(error)
        raise error
