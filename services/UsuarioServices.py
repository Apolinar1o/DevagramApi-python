from models.usuarioModel import UsuarioCriarModel
from providers.AwsProvider import AWSProvider
from repositories import usuarioRepositore
awsProvider = AWSProvider()
from repositories.usuarioRepositore import (
    listar_usuarios, criar_usuario, deletar_usuario, buscar_usuario_por_email, atualizar_usuario, buscar_usuario
)


async def registrar_usuario(usuario: UsuarioCriarModel, caminho_foto):

    try:
        usuario_encontrado = await buscar_usuario_por_email(usuario.email)
        if(usuario_encontrado):

            return {
                "mensagem": f"Email ja cadastrado no sistema",
                "status": 400
            }
        else:

            novo_usuario = await criar_usuario(usuario)

            url_foto = awsProvider.upload_arquivo_s3(
                    f"fotos-perfil/{novo_usuario["id"]}.png",
                    caminho_foto)
            novo_usuario = await atualizar_usuario(novo_usuario["id"], {"foto": url_foto})

            return {
                    "mensagem": "Usuario encontrado com sucesso",
                    "dados": novo_usuario,
                    "status": 201
            }


    except Exception as error:

        return {
            "mensagem": "Erro interno no servidor",
            "dados": str(error),
            "status": 500
        }
async def buscar_usuario(id: str):
    try:
            usuario_encontrado = await usuarioRepositore.buscar_usuario(id)
            if (usuario_encontrado):

                return usuario_encontrado
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

