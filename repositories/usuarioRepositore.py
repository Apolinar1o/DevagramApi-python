print("entrou")

import motor.motor_asyncio
from bson import ObjectId
from decouple import config
print("000000000000")
from models.usuarioModel import UsuarioModel, UsuarioCriarModel
from services.AuthService import gerar_senha_criptografada

MONGODB_URL=config("MONGODB_URL")

client = motor.motor_asyncio.AsyncIOMotorClient(MONGODB_URL)

database = client.devagram

usuario_collection = database.get_collection("usuario")

def usuario_helper(usuario):
    return {
        "id": str(usuario["_id"]),
        "nome": usuario["nome"],
        "email": usuario["email"],
        "senha": usuario["senha"],
        "foto": usuario["foto"]
    }
async def criar_usuario(usuario: UsuarioCriarModel) -> dict:
    usuario.senha = gerar_senha_criptografada(usuario.senha)

    usuario_criado = await usuario_collection.insert_one(usuario.__dict__)

    novo_usuario = await usuario_collection.find_one({"_id": usuario_criado.inserted_id})

    return usuario_helper((novo_usuario))


async def listar_usuarios():
   return usuario_collection.find()

async def buscar_usuario_por_email(email: str) -> dict:
    print("buscar?")
    usuario = await usuario_collection.find_one({"email": email})
    if usuario:
        return usuario_helper(usuario)

async def atualizar_usuario(id: str, dados_usuario):
    usuario = await usuario_collection.find_one({"id": ObjectId(str(id))})

    if( usuario):
        usuario_atualizado = await usuario_collection.update_one({
            "_id": ObjectId}, {"$set": dados_usuario
        })

        return usuario_helper(usuario_atualizado)
async def deletar_usuario(id: str):
    usuario = await usuario_collection.find_one({"id": ObjectId(str(id))})

    if( usuario):
        await usuario_collection.delete_one({"id": ObjectId(str(id))})