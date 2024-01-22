

class ConverterUtil:
    def usuario_helper(self, usuario):
        return {
            "id": str(usuario["_id"]),
            "nome": usuario["nome"],
            "email": usuario["email"],
            "senha": usuario["senha"],
            "foto": usuario["foto"] if "foto" in usuario else ""
        }

    def postagem_helper(self, postagem):
        return {
            "id": str(postagem["_id"]) if "_id" in postagem else "",
            "usuario": postagem["usuario"] if "usuario" in postagem else "",
            "foto": postagem["foto"] if "foto" in postagem else "",
            "legenda": postagem["legenda"] if "legenda" in postagem else "",
            "data": postagem["data"] if "data" in postagem else "",
            "curtidas": postagem["curtidas"] if "curtidas" in postagem else "",
            "comentarios": postagem["comentarios"] if "comentarios" in postagem else "",
            "usuario": self.usuario_helper(postagem["usuario"][0] if len(postagem["usuario"]) > 0 else "")

        }