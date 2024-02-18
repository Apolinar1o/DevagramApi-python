
import motor.motor_asyncio
from bson import ObjectId
from decouple import config
from models.usuarioModel import UsuarioModel, UsuarioCriarModel
from utils.AuthUtil import AuthUtil
from utils.ConverterUtil import ConverterUtil

MONGODB_URL: object=config("mongodb_url")

client = motor.motor_asyncio.AsyncIOMotorClient(MONGODB_URL)

database = client.devagram

usuario_collection = database.get_collection("usuario")
converterUtil = ConverterUtil()
authUtil = AuthUtil()

class UsuarioRepository:

    async def criar_usuario(self, usuario: UsuarioCriarModel) -> dict:
        usuario.senha = authUtil.gerar_senha_criptografada(usuario.senha)

        usuario_dict = {
            'nome': usuario.nome,
            "email": usuario.email,
            "senha": usuario.senha,
            "seguidores": [],
            "seguindo": []
        }

        usuario_criado = await usuario_collection.insert_one(usuario_dict)

        novo_usuario = await usuario_collection.find_one({"_id": usuario_criado.inserted_id})

        return converterUtil.usuario_helper((novo_usuario))


    async def listar_usuarios(self, nome ):
        usuarios_encontrados = usuario_collection.find({
            "nome": {
                '$regex': nome,
                "$options": "i"
            }
        })

        usuarios = []

        async for usuario in usuarios_encontrados:
            usuarios.append(converterUtil.usuario_helper(usuario))
        return usuarios
    async def buscar_usuario_por_email(self, email: str) -> dict:
        print("buscar?")
        usuario = await usuario_collection.find_one({"email": email})
        if usuario:
            return converterUtil.usuario_helper(usuario)

    async def atualizar_usuario(self, id: str, dados_usuario: dict) -> dict:
        if "senha" in dados_usuario:
            dados_usuario["senha"] = authUtil.gerar_senha_criptografada(dados_usuario["senha"])
        usuario = await usuario_collection.find_one({"_id": ObjectId(str(id))})

        if usuario:
            try:
                await usuario_collection.update_one(
                    {"_id": ObjectId(id)},
                    {"$set": dados_usuario}
                )

                usuario_atualizado = await usuario_collection.find_one({"_id": ObjectId(id)})
                return converterUtil.usuario_helper(usuario_atualizado)

            except Exception as error:
                    print(error)

    async def deletar_usuario(self, id: str):
        usuario = await usuario_collection.find_one({"_id": ObjectId(str(id))})

        if( usuario):
            await usuario_collection.delete_one({"_id": ObjectId(str(id))})

    async def buscar_usuario(self, id: str) -> dict:
        print("id: ", id)
        usuario = await usuario_collection.find_one({"_id": ObjectId(id)})
        print("usuario: ", usuario)
        if(usuario):
            return converterUtil.usuario_helper(usuario)
        else:
            return None
