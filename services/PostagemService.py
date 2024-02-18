from bson import ObjectId

from dto.ResponseDto import ResponseDto
from models.usuarioModel import UsuarioCriarModel, UsuarioAtualizarModel
from providers.AwsProvider import AWSProvider
import os
from repositories import usuarioRepositore
from repositories.PostagemRepository import PostagemRepository
from datetime import datetime



awsProvider = AWSProvider()
postagemRepository = PostagemRepository()

class PostagemService():
    async def cadastrar_postagem(self, postagem, usuario):
        try:
            postagem_criada  = await postagemRepository.criar_postagem(postagem, usuario)

            caminho_arquivo = f"files/foto-{datetime.now().strftime("%H%M%S")}.png"

            with open(caminho_arquivo, "wb+") as arquivo:
                arquivo.write(postagem.foto.file.read())
            url_foto = awsProvider.upload_arquivo_s3(
                f"fotos-postagem/{postagem_criada["id"]}.png",
                caminho_arquivo)

            nova_postagem = await postagemRepository.atualizar_postagem(postagem_criada["id"], {"foto": url_foto})

            os.remove(caminho_arquivo)

            return ResponseDto(mensagem="Postagens criada com sucesso!", dados=nova_postagem, status=201)


        except Exception as error:
            return ResponseDto(mensagem="Erro interno no servidor", dados=str(error),status= 500)

    async def listar_postagens(self):
        try:
            postagens = await postagemRepository.listar_postagens()
            for p in postagens:
                p["total_curtidas"] = len(p["curtidas"])

            return ResponseDto(mensagem="Postagens listadas com sucesso", dados=postagens, status=201)


        except Exception as error:
            print(error)
            return ResponseDto(mensagem="Erro interno no servidor", dados=str(error),status= 500)


    async def listar_postagens_usuario (self, usuario_id):
        try:
            print("usuario_id: ", usuario_id)
            postagens = await postagemRepository.listar_postagens_usuario(usuario_id)
            if postagens:
                for p in postagens:
                    p["total_curtidas"] = len(p["curtidas"])
                    p["total_comentarios"] = len(p["comentarios"])
                return ResponseDto(mensagem="Postagens listadas com sucesso", dados=postagens, status=201)

            else:
                return ResponseDto(mensagem="Postagens nãp eoncontrada",dados= "", status=404)

        except Exception as error:
            print(error)
            return ResponseDto(mensagem="Erro interno no servidor",dados= str(error),status= 500)


    async def curtir_descurtir(self, postagem_id, usuario_id):
        try:
            ret =1
            postagem_encontrada = await postagemRepository.buscar_postagem(postagem_id)

            if(usuario_id in postagem_encontrada["curtidas"]):

                postagem_encontrada["curtidas"].remove(usuario_id)

            else:
                ret = 2
                postagem_encontrada["curtidas"].append(ObjectId(usuario_id))

            postagem_atualizada = await postagemRepository.atualizar_postagem(postagem_encontrada["id"], {"curtidas":postagem_encontrada["curtidas"]})

            if(ret == 2):
                return ResponseDto(mensagem="Postagem curtida com sucesso", dados=postagem_atualizada,status= 201)

            return ResponseDto(mensagem="Postagem descurtida com sucesso", dados=postagem_atualizada, status=201)


        except Exception as error:
            print("deu erro ao curtir: ", error)
            return ResponseDto(mensagem="Erro interno no servidor",dados= str(error), status=500)


    async def deletar_postagem(self, postagem_id, usuario_id):
        try:
            postagem_encontrada = await postagemRepository.buscar_postagem(postagem_id)
            if not postagem_encontrada["usuario_id"] == (usuario_id):
                return ResponseDto(mensagem="Não é possivel realizar essa requisição",dados= "", status=401)
            await postagemRepository.deletar_postagem(postagem_id)

            return ResponseDto(mensagem="Postagem deletado com sucesso", dados="", status=201)

        except Exception as error:
            print(error)
            return ResponseDto(mensagem="Erro interno no servidor", dados=str(error),status= 500)


    async def criar_comentario(self, postagem_id, usuario_id, comentario):
            try:
                postagem_encontrada = await postagemRepository.buscar_postagem(postagem_id)

                postagem_encontrada["comentarios"].append({
                    "comentario_id": ObjectId(),
                    'usuario_id': ObjectId(usuario_id),
                    "comentario": comentario
                })

                postagem_atualizada = await postagemRepository.atualizar_postagem(
                    postagem_encontrada["id"], {"comentarios":postagem_encontrada["comentarios"]})

                return ResponseDto(mensagem="Comentário criada com sucesso", dados=postagem_atualizada,status= 201)

            except Exception as error:
                print("deu erro: ", error)
                return ResponseDto(mensagem="Erro interno no servidor", dados=str(error),status= 500)

    async def deletar_comentario(self, postagem_id, usuario_id, comentario_id):
        deletar = 0
        try:

            postagem_encontrada = await postagemRepository.buscar_postagem(postagem_id)
            if(postagem_encontrada["comentarios"] == []):
                return ResponseDto(mensagem="comentario não encontrado", dados="", status=401)

            for comentario in postagem_encontrada["comentarios"]:
                if comentario["comentario_id"] == comentario_id:
                    if not (comentario["usuario_id"] == usuario_id or postagem_encontrada["usuario_id"] == usuario_id):
                        return ResponseDto(mensagem="impossivel apagar esse comentario", dados="",status= 401)

                    postagem_encontrada["comentarios"].remove(comentario)
                    deletar = 1


            if(deletar == 1):

                postagem_atualizada = await postagemRepository.atualizar_postagem(
                    postagem_encontrada["id"], {"comentarios": postagem_encontrada["comentarios"]})

                return ResponseDto(mensagem="Comentário deletado com sucesso",dados= postagem_atualizada,status= 201)

            raise Exception("Não foi possível deletar.")

        except Exception as error:
            return ResponseDto(mensagem="Erro interno no servidor", dados=str(error), status=500)

    async def atualizar_comentario(self, postagem_id, usuario_id, comentario_id, comentario_atualizado):
            atualizar = 0
            try:

                postagem_encontrada = await postagemRepository.buscar_postagem(postagem_id)
                if (postagem_encontrada["comentarios"] == []):
                    return ResponseDto(mensagem="comentario não encontrado", dados="", status=401)

                for comentario in postagem_encontrada["comentarios"]:
                    if comentario["comentario_id"] == comentario_id:
                        if not comentario["usuario_id"] == usuario_id:
                            return ResponseDto("Comentário atualizado com sucesso", "", 401)
                        atualizar = 1
                        comentario["comentario"] = comentario_atualizado
                if atualizar == 1:

                    postagem_atualizada = await postagemRepository.atualizar_postagem(
                        postagem_encontrada["id"], {"comentarios": postagem_encontrada["comentarios"]})
                    return ResponseDto(mensagem="Comentário criada com sucesso",dados= postagem_atualizada,status= 201)
                raise Exception("impossivel de atualizar")
            except Exception as error:
                print("deu erro: ", error)
                return ResponseDto(mensagem="Erro interno no servidor",dados= str(error), status=500)

