from models.usuarioModel import UsuarioCriarModel
from repositories.usuarioRepositore import (
    listar_usuarios, criar_usuario, deletar_usuario, buscar_usuario_por_email, atualizar_usuario
)


async def registrar_usuario(usuario: UsuarioCriarModel):

    try:
        usuario_encontrado = await buscar_usuario_por_email(usuario.email)
        if(usuario_encontrado):

            return {
                "mensagem": f"Email ja cadastrado no sistema",
                "status": 400
            }
        else:

            novo_usuario = await criar_usuario(usuario)
            
            return {
                "mensagem": "Usuario encontrado com sucesso",
                "dados": novo_usuario,
                "status": 201
            }
    except Exception as error:
        print("444444444444444444444")

        return {
            "mensagem": "Erro interno no servidor",
            "dados": str(error),
            "status": 500
        }