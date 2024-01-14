from passlib.context import CryptContext
from models.usuarioModel import UsuarioLoginModel
print("authService?")
from repositories.usuarioRepositore import buscar_usuario_por_email
print("auth")
pwd_context = CryptContext(schemes=["bcrypt"], deprecated="auto")
print("authService")
async def login_service(usuario: UsuarioLoginModel):
    usuario_encontrado = await buscar_usuario_por_email(usuario.email)

    if(not usuario):
        return{
            "mensagem": "email ou senha incorretos",
            "dados": "",
            "status": 401
        }
    else:
        if( verificar_senha(usuario.senha, usuario_encontrado.senha)):
            return {
                "mensagem": "Login realizado com sucesso",
                "dados": usuario_encontrado,
                "status": 200
            }
        else:
            return {
                "mensagem": "email ou senha incorretos"
            }
def gerar_senha_criptografada(senha):
    return pwd_context.hash(senha)
def verificar_senha(senha, senha_criptografada):
    return pwd_context.verify(senha, senha_criptografada)