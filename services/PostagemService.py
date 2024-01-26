from bson import ObjectId

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

            return {
                "mensagem": "Postagem criada com sucesso",
                "dados": nova_postagem,
                "status": 201
            }

        except Exception as error:

            return {
                "mensagem": "Erro interno no servidor",
                "dados": str(error),
                "status": 500
            }
    async def listar_postagens(self):
        try:
            postagens = await postagemRepository.listar_postagens()
            for p in postagens:
                p["total_curtidas"] = len(p["curtidas"])

            return {
                 "mensagem": "Postagens listadas com sucesso",
                 "dados": postagens,
                 "status": 200
            }

        except Exception as error:
            print(error)
            return{
               "mensagem": "Erro interno no servidor",
               "dados": str(error),
               "status": 500
            }

    async def curtir_descurtir(self, postagem_id, usuario_id):
        try:
            postagem_encontrada = await postagemRepository.buscar_postagem(postagem_id)

            if(usuario_id in postagem_encontrada["curtidas"]):
                postagem_encontrada["curtidas"].remove(usuario_id)

            else:
                postagem_encontrada["curtidas"].append(ObjectId(usuario_id))

            postagem_atualizada = await postagemRepository.atualizar_postagem(postagem_encontrada["id"], {"curtidas":postagem_encontrada["curtidas"]})


            return {
                "mensagem": "Postagem criada com sucesso",
                "dados": postagem_atualizada,
                "status": 201
            }

        except Exception as error:
            print("deu erro: ", error)
            return {
                "mensagem": "Erro interno no servidor",
                "dados": str(error),
                "status": 500
            }
    async def criar_comentario(self, postagem_id, usuario_id, comentario):
            try:
                postagem_encontrada = await postagemRepository.buscar_postagem(postagem_id)

                postagem_encontrada["comentarios"].append({
                    'usuario_id': ObjectId(usuario_id),
                    "comentario": comentario
                })

                postagem_atualizada = await postagemRepository.atualizar_postagem(
                    postagem_encontrada["id"], {"comentarios":postagem_encontrada["comentarios"]})


                return {
                    "mensagem": "Comentário criada com sucesso",
                    "dados": postagem_atualizada,
                    "status": 201
                }

            except Exception as error:
                print("deu erro: ", error)
                return {
                    "mensagem": "Erro interno no servidor",
                    "dados": str(error),
                    "status": 500
                }



