from typing import List

from pydantic import BaseModel, Field

from models.ComentariosModel import ComentarioModel
from models.usuarioModel import UsuarioModel


class PostagemModel(BaseModel):
    id: str= Field(...)
    usuario: UsuarioModel = Field(...)
    foto: str= Field(...)
    legenda: str = Field(...)
    data: str = Field(...)
    curtidas: str = Field(...)
    comentarios: List[ComentarioModel] = Field(...)

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

class PostagemCriarModel(BaseModel):
    usuario: UsuarioModel = Field(...)
    foto: str= Field(...)
    legenda: str = Field(...)

    class Config:
        Schema_extra = {
            "postagem": {
                "usuario": "UsuarioModel",
                "foto": "string",
                "legenda": "string",
            }
        }