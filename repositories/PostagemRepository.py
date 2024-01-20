import motor.motor_asyncio
from bson import ObjectId
from decouple import config
from utils.ConverterUtil import ConverterUtil
from models.PostagemModel import PostagemCriarModel
from models.usuarioModel import UsuarioModel, UsuarioCriarModel
from utils.AuthUtil import gerar_senha_criptografada

MONGODB_URL=config("MONGODB_URL")

client = motor.motor_asyncio.AsyncIOMotorClient(MONGODB_URL)

database = client.devagram

postagem_collection = database.get_collection("postagem")

converterUtil = ConverterUtil()
class PostagemRepository:
    async def criar_postagem (self, postagem: PostagemCriarModel) -> dict:

        postagem_criada = await postagem_collection.insert_one(postagem.__dict__)

        nova_postagem = await postagem_collection.find_one({"_id": postagem_criada.inserted_id})

        return converterUtil.postagem_converter((postagem_criada))
    async def listar_postagens(self):
       return postagem_collection.find()

    async def buscar_postagem(self, id: str) -> dict:
        postagem = await postagem_collection.find_one({"_id": ObjectId(id)})

        if(postagem):
            return converterUtil.postagem_converter(postagem)

    async def buscar_postagem_por_email(self, email: str) -> dict:
        print("buscar?")
        postagem = await postagem_collection.find_one({"email": email})
        if postagem:
            return converterUtil.postagem_converter(postagem)

    async def atualizar_postagem(self, id: str, dados_usuario: dict) -> dict:

        postagem = await postagem_collection.find_one({"_id": ObjectId(str(id))})

        if postagem:
            try:
                await postagem.update_one(
                    {"_id": ObjectId(id)},
                    {"$set": dados_usuario}
                )

                postagem_atualizada = await postagem_collection.find_one({"_id": ObjectId(id)})

                return converterUtil.postagem_converter(postagem_atualizada)

            except Exception as error:
                    print(error)

    async def deletar_postagem(self, id: str):
        postagem = await postagem_collection.find_one({"_id": ObjectId(str(id))})

        if( postagem):
            await postagem_collection.delete_one({"_id": ObjectId(str(id))})
