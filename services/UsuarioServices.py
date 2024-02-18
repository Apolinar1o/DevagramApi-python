from bson import ObjectId

from dto.ResponseDto import ResponseDto
from models.usuarioModel import UsuarioCriarModel, UsuarioAtualizarModel
from providers.AwsProvider import AWSProvider
from repositories import usuarioRepositore
from repositories.PostagemRepository import PostagemRepository
from repositories.usuarioRepositore import UsuarioRepository
from datetime import datetime
import os




awsProvider = AWSProvider()
UsuarioRepository = UsuarioRepository()
PostagemRepository = PostagemRepository()

class UsuarioService():
    async def registrar_usuario(self, usuario: UsuarioCriarModel, caminho_foto):
    
        try:
            usuario_encontrado = await UsuarioRepository.buscar_usuario_por_email(usuario.email)
            if(usuario_encontrado):
                return ResponseDto(mensagem="Email ja cadastrado", dados="", status=201)

            else:
    
                novo_usuario = await UsuarioRepository.criar_usuario(usuario)
                url_foto = awsProvider.upload_arquivo_s3(
                        f"fotos-perfil/{novo_usuario["id"]}.png",
                        caminho_foto)
                novo_usuario = await UsuarioRepository.atualizar_usuario(novo_usuario["id"], {"foto": url_foto})


                return ResponseDto(mensagem="Usuario encontrado com sucesso", dados=novo_usuario, status=201)

    
    
        except Exception as error:
            print(error)
            return ResponseDto(mensagem="Erro interno no servidor", dados =str(error), status=500)
    async def buscar_usuario(self, id: str):
        try:

                usuario_encontrado = await UsuarioRepository.buscar_usuario(id)
                postagens = await PostagemRepository.listar_postagens_usuario(id)

                usuario_encontrado["total_seguidores"] = len(usuario_encontrado["seguidores"])
                usuario_encontrado["total_seguindo"] = len(usuario_encontrado["seguindo"])
                usuario_encontrado["postagens"] = postagens
                usuario_encontrado["total_postagens"] = len(usuario_encontrado["postagens"])

                print("22222222222222222222222222222")
                if (usuario_encontrado):
                    return ResponseDto(mensagem="Usuario encontrado", dados=usuario_encontrado, status=200)


                else:
                    return ResponseDto(mensagem="Usuário com o id {id} não foi encontrado", dados="", status=404)



        except Exception as error:
            print(error)
            return ResponseDto(mensagem="Erro interno no servidor", dados=str(error), status=500)


    async def listar_usuarios(self, nome):
        try:
                usuarios_encontrado = await UsuarioRepository.listar_usuarios(nome)
                if (usuarios_encontrado):
                    for usuario in usuarios_encontrado:
                        usuario["total_seguindo"] = len(usuario["seguindo"])
                        usuario["total_seguidores"] = len(usuario["seguidores"])

                    return ResponseDto(mensagem="Usuarios encontrados", dados=usuarios_encontrado, status=200)



                else:

                    return ResponseDto(mensagem = "erro ao encontrar usuario.",dados = "", status = 404)

        except Exception as error:
            print(error)
            return ResponseDto(mensagem= "Erro interno no servidor", dados= str(error), status = 500)



    async def atualizar_usuario_logado(self,id,  dadosUsuario: UsuarioAtualizarModel):
        try:

                usuario_encontrado = await UsuarioRepository.buscar_usuario(id)

                if (usuario_encontrado):
                    usuario_dict = dadosUsuario.__dict__

                    try:
                        caminho_arquivo = f"files/foto-{datetime.now().strftime("%H%M%S")}.png"

                        with open(caminho_arquivo, "wb+") as arquivo:
                            arquivo.write(dadosUsuario.foto.file.read())

                        url_foto = awsProvider.upload_arquivo_s3(
                            f"fotos-perfil/{id}.png",
                            caminho_arquivo)
                        os.remove(caminho_arquivo)
                    except Exception as erro:
                        print(erro)

                    usuario_dict["foto"] = url_foto if not url_foto is None else usuario_dict["foto"]
                    usuario_atualizado = await UsuarioRepository.atualizar_usuario(id, usuario_dict)

                    return ResponseDto(mensagem= "Usuario atualizado", dados=usuario_atualizado,status= 200)

                else:
                    return ResponseDto(mensagem="Usuário com o id {id} não foi encontrado.", dados="",status= 404)

        except Exception as error:
            print(error)
            return ResponseDto(mensagem="Erro interno no servidor.",dados= str(error),status= 500)

    async def seguir_usuario(self, usuario_logado_id, usuario_id):
        try:
            seguindo = 0
            usuario_encontrado = await UsuarioRepository.buscar_usuario(usuario_id)
            usuario_logado_encontrado = await UsuarioRepository.buscar_usuario(usuario_logado_id)

            if(usuario_logado_id in usuario_encontrado["seguidores"]):
                seguindo = 1
                usuario_encontrado["seguidores"].remove((usuario_logado_id))
                usuario_logado_encontrado["seguindo"].remove((usuario_id))


            else:
                usuario_logado_encontrado["seguindo"].append(str(ObjectId(usuario_id)))
                usuario_encontrado["seguidores"].append(str(ObjectId(usuario_logado_id)))



            await UsuarioRepository.atualizar_usuario(
                 usuario_encontrado["id"],
                {
                    "seguidores":usuario_encontrado["seguidores"]
                })

            await UsuarioRepository.atualizar_usuario(
                usuario_logado_encontrado["id"],
                {
                    "seguindo": usuario_logado_encontrado["seguindo"]
                })
            if(seguindo == 1):
                return ResponseDto(mensagem="unfollow realizado com sucesso", dados="", status=201)

            return ResponseDto(mensagem="Usuario seguido com sucesso", dados="", status=201)

        except Exception as error:
            print("deu erro ao seguir usuario: ", error)
            return ResponseDto(mensagem="deu erro ao seguir usuario",dados= str(error), status=500)


