import time
import jwt
from decouple import config
from models.usuarioModel import UsuarioLoginModel
from repositories.usuarioRepositore import buscar_usuario_por_email
from utils.AuthUtil import verificar_senha

JWT_SECRET = config("JWT_SECRET")

def gerar_token_jwt(usuario_id: str) -> str:
    payload ={
        "usuario_id": usuario_id,
        "expires": time.time() + 600
    }


    token = jwt.encode(payload, JWT_SECRET, algorithm="HS256" )
    return token
def decodificar_token_jwt(token: str):
    try:
        token_decodificado = jwt.decode(token, JWT_SECRET, algorithms=["HS256"])

        if token_decodificado["expires"] >= time.time():
            return token_decodificado
        else:
            return None
    except Exception as erro:
        return None


async def login_service(usuario: UsuarioLoginModel):
    usuario_encontrado = await buscar_usuario_por_email(usuario.email)

    if(not usuario_encontrado):
        return{
            "mensagem": "email ou senha incorretos",
            "dados": "",
            "status": 401
        }
    else:
        if verificar_senha(usuario.senha, usuario_encontrado['senha']):

            return {
                "mensagem": "Login realizado com sucesso",
                "dados": usuario_encontrado,
                "status": 200
            }
        else:
            return {
                "mensagem": "email ou senha incorretos",
                "status": 500
            }
