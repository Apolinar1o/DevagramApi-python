from typing import List
from fastapi import UploadFile
from pydantic import BaseModel, Field
from models.usuarioModel import UsuarioModel
from utils.DecoratorUtil import decoratorUtil
decoratorUtil = decoratorUtil

class PostagemModel(BaseModel):
    id: str= Field(...)
    usuario: UsuarioModel = Field(...)
    foto: str= Field(...)
    legenda: str = Field(...)
    data: str = Field(...)
    curtidas: str = Field(...)
    comentarios: List = Field(...)

    class Config:
        Schema_extra = {
            "postagem": {
                "id": "string",
                "foto": "string",
                "legenda": "string",
                "data": "date",
                "curtidas": "int,",
                "comentarios": "List[comentarios]"
            }
        }
@decoratorUtil.form_body
class PostagemCriarModel(BaseModel):
    foto: UploadFile = Field(...)
    legenda: str = Field(...)

    class Config:
        Schema_extra = {
            "postagem": {
                "foto": "string",
                "legenda": "string",
            }
        }