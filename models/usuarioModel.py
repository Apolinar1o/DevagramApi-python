from fastapi import Form, UploadFile
from pydantic import BaseModel, Field, EmailStr
from utils.DecoratorUtil import decoratorUtil

decoratorUtil = decoratorUtil
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



@decoratorUtil.form_body
class UsuarioCriarModel(BaseModel):
    nome: str = Field(max_length=8)
    email: EmailStr = Field(...)
    senha: str = Field(...)

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
@decoratorUtil.form_body
class UsuarioAtualizarModel(BaseModel):
    nome: str = Field(...)
    email: EmailStr = Field(...)
    senha: str = Field(...)
    foto: UploadFile = Field(...)

    class Config:
        Schema_extra = {
                "usuario": {
                "email": "fulano@gmail.com",
                "senha": "Senha123@",

            }
        }


