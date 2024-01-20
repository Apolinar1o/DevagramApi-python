
import motor.motor_asyncio
from bson import ObjectId
from decouple import config
from models.usuarioModel import UsuarioModel, UsuarioCriarModel
from utils.AuthUtil import gerar_senha_criptografada
from utils.ConverterUtil import ConverterUtil

MONGODB_URL=config("MONGODB_URL")

client = motor.motor_asyncio.AsyncIOMotorClient(MONGODB_URL)

database = client.devagram

usuario_collection = database.get_collection("usuario")


converterUtil = ConverterUtil()
class UsuarioRepository:

    async def criar_usuario(self, usuario: UsuarioCriarModel) -> dict:
        usuario.senha = gerar_senha_criptografada(usuario.senha)

        usuario_criado = await usuario_collection.insert_one(usuario.__dict__)

        novo_usuario = await usuario_collection.find_one({"_id": usuario_criado.inserted_id})

        return converterUtil.usuario_converter(novo_usuario)


    async def listar_usuarios(self):
       return usuario_collection.find()

    async def buscar_usuario_por_email(self, email: str) -> dict:
        print("buscar?")
        usuario = await usuario_collection.find_one({"email": email})
        if usuario:
            return converterUtil.usuario_converter(usuario)

    async def atualizar_usuario(self, id: str, dados_usuario: dict) -> dict:

        usuario = await usuario_collection.find_one({"_id": ObjectId(str(id))})

        if usuario:
            try:
                await usuario_collection.update_one(
                    {"_id": ObjectId(id)},
                    {"$set": dados_usuario}
                )

                usuario_atualizado = await usuario_collection.find_one({"_id": ObjectId(id)})

                return converterUtil.usuario_converter(usuario_atualizado)

            except Exception as error:
                    print(error)

    async def deletar_usuario(self, id: str):
        usuario = await usuario_collection.find_one({"_id": ObjectId(str(id))})

        if( usuario):
            await usuario_collection.delete_one({"_id": ObjectId(str(id))})

    async def buscar_usuario(self, id: str) -> dict:
        usuario = await usuario_collection.find_one({"_id": ObjectId(id)})

        if(usuario):
            return converterUtil.usuario_converter(usuario)
