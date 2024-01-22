from datetime import datetime

import motor.motor_asyncio
from bson import ObjectId
from decouple import config

from models.PostagemModel import PostagemCriarModel
from models.usuarioModel import UsuarioModel, UsuarioCriarModel
from utils.AuthUtil import gerar_senha_criptografada
from utils.ConverterUtil import ConverterUtil

MONGODB_URL=config("MONGODB_URL")

client = motor.motor_asyncio.AsyncIOMotorClient(MONGODB_URL)

database = client.devagram

postagem_collection = database.get_collection("postagem")
converterUtil = ConverterUtil()
class PostagemRepository:
    async def criar_postagem (self, postagem: PostagemCriarModel, usuario_id) -> dict:
        postagem_dict= {
            "usuario_id": ObjectId(usuario_id),
            "legenda": postagem.legenda,
            "curtidas": [],
            "comentarios": [],
            "data": datetime.now( )
        }

        postagem_criada = await postagem_collection.insert_one(postagem_dict)

        nova_postagem = await postagem_collection.find_one({"_id": postagem_criada.inserted_id})

        return converterUtil.postagem_helper(nova_postagem)
    async def listar_postagens(self):
        postagens_encontradas = postagem_collection.aggregate([{
            "$lookup": {
                "from": "usuario",
                "localField": "usuario_id",
                "foreignField": "_id",
                "as": "usuario"
            }
        }])
        postagens = []

        async for postagem in postagens_encontradas:
            postagens.append(converterUtil.postagem_helper(postagem))

        return postagens
    async def buscar_postagem(self, id: str) -> dict:
        postagem = await postagem_collection.find_one({"_id": ObjectId(id)})

        if(postagem):
            return converterUtil.postagem_helper(postagem)

    async def buscar_postagem_por_email(self, email: str) -> dict:
        print("buscar?")
        postagem = await postagem_collection.find_one({"email": email})
        if postagem:
            return converterUtil.postagem_helper(postagem)

    async def atualizar_postagem(self, id: str, dados_postagem: dict) -> dict:

        postagem = await postagem_collection.find_one({"_id": ObjectId(str(id))})

        if postagem:
            try:
                await postagem_collection.update_one(
                    {"_id": ObjectId(id)},
                    {"$set": dados_postagem}
                )
                postagem_atualizada = await postagem_collection.find_one({"_id": ObjectId(id)})

                return converterUtil.postagem_helper(postagem_atualizada)

            except Exception as error:
                    print(error)

    async def deletar_postagem(self, id: str):
        postagem = await postagem_collection.find_one({"_id": ObjectId(str(id))})

        if( postagem):
            await postagem_collection.delete_one({"_id": ObjectId(str(id))})
