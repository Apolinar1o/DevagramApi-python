from pydantic import BaseModel, Field

from models.PostagemModel import decoratorUtil


@decoratorUtil.form_body
class ComentarioModel(BaseModel):
    usuario: str = Field(...)
    comentario: str = Field(...)


@decoratorUtil.form_body
class ComentarioCriarModel(BaseModel):
    comentario: str = Field(...)