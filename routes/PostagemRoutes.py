from datetime import datetime
import os
from fastapi import APIRouter, HTTPException, Depends, Header, UploadFile, Body
from middleware.JwtMiddleWare import verificar_token
from models.ComentariosModel import ComentarioModel, ComentarioCriarModel, ComentarioAtualizarModel
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

        resultado = await authService.validar_usuario_logado(Authorization)

        usuario_logado = resultado.dados

        postagem = await postagemService.cadastrar_postagem(postagem, usuario_logado["id"])
        if not postagem.status == 201:
            raise HTTPException(status_code=postagem.status, detail=postagem.mensagem)

        return resultado.__dict__
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

        if not resultado.status == 201:
            raise HTTPException(status_code=resultado.status, detail=resultado.mensagem)
        return resultado.__dict__
    except:
        raise HTTPException(status_code=500, detail='Erro interno no servidor')

@router.get(
    "/postagem/{usuario_id}",
    response_description="Rota para buscar postagens do usuario especifico",
    dependencies=[Depends(verificar_token)]
)
async def listar_postagens_usuario(usuario_id: str):
    print("11111111111111111111111111111111")
    try:
        resultado = await postagemService.listar_postagens_usuario(usuario_id)
        if not resultado.status == 201:
            raise HTTPException(status_code=resultado.status, detail=resultado.mensagem)
        return resultado.__dict__
    except:
        raise HTTPException(status_code=500, detail='Erro interno no servidor')



@router.put(
    "/postagem/curtir/{postagem}",
    response_description="Rota para curtir e descurtir",
    dependencies=[Depends(verificar_token)]
)
async def curtir_descurtir(postagem: str, Authorization: str = Header(default="")):
    try:

        resultado = await authService.validar_usuario_logado(Authorization)

        user = resultado.dados["id"]
        comentario = await postagemService.curtir_descurtir(postagem, user)
        if not comentario.status== 201:
            raise HTTPException(status_code=comentario.status, detail=comentario.mensagem)
        return comentario.__dict__

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
        resultado = await authService.validar_usuario_logado(Authorization)

        user = resultado.dados["id"]
        comentario = await postagemService.criar_comentario(postagem, user, comentario)
        if not comentario.status == 201:
            raise HTTPException(status_code=comentario.status, detail=comentario.mensagem)
        return comentario.__dict__

    except Exception as error:
        print(error)
        raise error


@router.delete(
    "/postagem/{postagem_id}/comentario/{comentario_id}",
    response_description="Rota para deletar um comentario em uma postagem",
    dependencies=[Depends(verificar_token)]
)
async def deletar_comentario(postagem_id: str, comentario_id: str ,Authorization: str = Header(default="")):
    try:
        resultado = await authService.validar_usuario_logado(Authorization)

        user = resultado.dados["id"]

        deletar = await postagemService.deletar_comentario(postagem_id, user, comentario_id)
        if not deletar.status == 201:
            raise HTTPException(status_code=deletar.status, detail=deletar.dados)
        return deletar.__dict__

    except Exception as error:
        print(error)
        raise error
@router.put(
    "/postagem/{postagem_id}/comentario/{comentario_id}",
    response_description="Rota para atualizar um comentario em uma postagem",
    dependencies=[Depends(verificar_token)]
)
async def atualizar_comentario(postagem_id: str, comentario_id: str ,Authorization: str = Header(default=""), comentario_model: ComentarioAtualizarModel = Body(...)):
    try:
        resultado = await authService.validar_usuario_logado(Authorization)

        user = resultado.dados["id"]

        atualizar = await postagemService.atualizar_comentario(postagem_id, user, comentario_id, comentario_model.comentario)
        if not atualizar.status == 201:
            raise HTTPException(status_code=atualizar.status, detail=atualizar.mensagem)
        return atualizar.__dict__

    except Exception as error:
        print(error)
        raise error
@router.delete(
    "/postagem/{postagem_id}",
    response_description="Rota para deletar uma postagem",
    dependencies=[Depends(verificar_token)]
)
async def deletar_postagem(postagem_id: str ,Authorization: str = Header(default="")):
    try:
        resultado = await authService.validar_usuario_logado(Authorization)
        if not resultado.dados:
            return {
                "mensagem": "Postagem não encontrada",
                "dados": "",
                "status": 404
            }
        deletar = await postagemService.deletar_postagem(postagem_id, resultado.dados["id"])
        print("deletar: ",deletar.status)
        if not deletar.status == 201:
            raise HTTPException(status_code=deletar.status, detail=deletar.mensagem)
        return deletar.__dict__

    except Exception as error:
        print(error)
        raise error

