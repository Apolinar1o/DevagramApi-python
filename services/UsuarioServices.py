from models.usuarioModel import UsuarioCriarModel, UsuarioAtualizarModel
from providers.AwsProvider import AWSProvider
from repositories import usuarioRepositore
from repositories.usuarioRepositore import UsuarioRepository
from datetime import datetime
import os




awsProvider = AWSProvider()
UsuarioRepository = UsuarioRepository()

class UsuarioService():
    async def registrar_usuario(self, usuario: UsuarioCriarModel, caminho_foto):
    
        try:
            usuario_encontrado = await UsuarioRepository.buscar_usuario_por_email(usuario.email)
            if(usuario_encontrado):
    
                return {
                    "mensagem": f"Email ja cadastrado no sistema",
                    "status": 400
                }
            else:
    
                novo_usuario = await UsuarioRepository.criar_usuario(usuario)
    
                url_foto = awsProvider.upload_arquivo_s3(
                        f"fotos-perfil/{novo_usuario["id"]}.png",
                        caminho_foto)
                novo_usuario = await UsuarioRepository.atualizar_usuario(novo_usuario["id"], {"foto": url_foto})

                os.remove(caminho_foto)
                return {
                        "mensagem": "Usuario encontrado com sucesso",
                        "dados": novo_usuario,
                        "status": 201
                }
    
    
        except Exception as error:
            print(error)
            return {
                "mensagem": "Erro interno no servidor",
                "dados": str(error),
                "status": 500
            }
    async def buscar_usuario(self, id: str):
        try:
                usuario_encontrado = await UsuarioRepository.buscar_usuario(id)
                if (usuario_encontrado):

                    return {
                        "mensagem": f"Usuario encontrado",
                        "dados": usuario_encontrado,
                        "status": 200
                    }

                else:
                    return {
                        "dados": "",
                        "mensagem": f"Usuário com o id {id} não foi encontrado.",
                        "status": 404
                    }
        except Exception as error:
            print(error)
            return {
                "mensagem": "Erro interno no servidor",
                "dados": str(error),
                "status": 500
            }
    
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

                    return {
                        "mensagem": f"Usuario atualizado",
                        "dados": usuario_atualizado,
                        "status": 200
                    }

                else:
                    return {
                        "dados": "",
                        "mensagem": f"Usuário com o id {id} não foi encontrado.",
                        "status": 404
                    }
        except Exception as error:
            print(error)
            return {
                "mensagem": "Erro interno no servidor",
                "dados": str(error),
                "status": 500
            }
