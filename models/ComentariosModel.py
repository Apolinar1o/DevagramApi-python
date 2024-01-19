from pydantic import BaseModel, Field

from models.usuarioModel import UsuarioModel


class ComentarioModel(BaseModel):
    usuario: UsuarioModel = Field(...)
    comentario = str = Field(...)
