from pydantic import BaseModel, Field, EmailStr

class UsuarioModel(BaseModel):
    id: str = Field(...)
    nome: str = Field(...)
    email: EmailStr = Field(...)
    senha: str = Field(...)
    foto: str= Field(...)

    class Config:
        Schema_extra = {
                "usuario": {
                "nome": "Fulano de tal",
                "email": "fulano@gmail.com",
                "senha": "Senha123@",
                "foto": "fulano.png"
            }
        }

class UsuarioCriarModel(BaseModel):
    nome: str = Field(...)
    email: EmailStr = Field(...)
    senha: str = Field(...)
    foto: str= Field(...)

    class Config:
        Schema_extra = {
                "usuario": {
                "nome": "Fulano de tal",
                "email": "fulano@gmail.com",
                "senha": "Senha123@",
                "foto": "fulano.png"
            }
        }
class UsuarioLoginModel(BaseModel):

    email: EmailStr = Field(...)
    senha: str = Field(...)


    class Config:
        Schema_extra = {
                "usuario": {
                "email": "fulano@gmail.com",
                "senha": "Senha123@",

            }
        }

