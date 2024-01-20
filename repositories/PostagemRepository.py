import motor.motor_asyncio
from bson import ObjectId
from decouple import config

from models.PostagemModel import PostagemCriarModel
from models.usuarioModel import UsuarioModel, UsuarioCriarModel
from utils.AuthUtil import gerar_senha_criptografada

MONGODB_URL=config("MONGODB_URL")

client = motor.motor_asyncio.AsyncIOMotorClient(MONGODB_URL)

database = client.devagram

postagem_collection = database.get_collection("postagem")

def postagem_helper(postagem):
    return {
        "id": str(postagem["_id"]) if "_id" in postagem else "",
        "usuario": postagem["usuario"] if "usuario" in postagem else "",
        "foto": postagem["foto"] if "foto" in postagem else "",
        "legenda": postagem["legenda"] if "legenda" in postagem else "",
        "data": postagem["data"] if "data" in postagem else "",
        "curtidas": postagem["curtidas"] if "curtidas" in postagem else "",
        "comentarios": postagem["comentarios"] if "comentarios" in postagem else "",

    }
async def criar_postagem (postagem: PostagemCriarModel) -> dict:

    postagem_criada = await postagem_collection.insert_one(postagem.__dict__)

    nova_postagem = await postagem_collection.find_one({"_id": postagem_criada.inserted_id})

    return postagem_helper((postagem_criada))
async def listar_postagens():
   return postagem_collection.find()

async def buscar_postagem(id: str) -> dict:
    postagem = await postagem_collection.find_one({"_id": ObjectId(id)})

    if(postagem):
        return postagem_helper(postagem)

async def buscar_postagem_por_email(email: str) -> dict:
    print("buscar?")
    postagem = await postagem_collection.find_one({"email": email})
    if postagem:
        return postagem_helper(postagem)
    
async def atualizar_postagem(id: str, dados_usuario: dict) -> dict:

    postagem = await postagem_collection.find_one({"_id": ObjectId(str(id))})

    if postagem:
        try:
            await postagem.update_one(
                {"_id": ObjectId(id)},
                {"$set": dados_usuario}
            )

            postagem_atualizada = await postagem_collection.find_one({"_id": ObjectId(id)})

            return postagem_helper(postagem_atualizada)

        except Exception as error:
                print(error)

async def deletar_postagem(id: str):
    postagem = await postagem_collection.find_one({"_id": ObjectId(str(id))})

    if( postagem):
        await postagem_collection.delete_one({"_id": ObjectId(str(id))})
