

class ConverterUtil:
    def usuario_helper(self, usuario):
        return {
            "id": str(usuario["_id"]) if "_id" in usuario else "",
            "nome": str(usuario["nome"]) if "nome" in usuario else "",
            "email": str(usuario["email"]) if "email" in usuario else "",
            "senha": str(usuario["senha"]) if "senha" in usuario else "",
            "foto": usuario["foto"] if "foto" in usuario else "",
            "seguidores": [str(p) for p in usuario["seguidores"]] if "seguidores" in usuario else [],
            "seguindo": [str(p) for p in usuario["seguindo"]] if "seguindo" in usuario else [],
            "total_seguidores": len(usuario["seguidores"]) if "total_seguidores" in usuario else 0,
            "total_seguindo": len(usuario["seguindo"]) if "total_seguindo" in usuario else 0,

        }

    def postagem_helper(self, postagem):
        return {
            "id": str(postagem["_id"]) if "_id" in postagem else "",
            "usuario_id": str(postagem["usuario_id"]) if "usuario_id" in postagem else "",
            "foto": postagem["foto"] if "foto" in postagem else "",
            "legenda": postagem["legenda"] if "legenda" in postagem else "",
            "data": postagem["data"] if "data" in postagem else "",
            "curtidas": [str(p) for p in postagem["curtidas"]] if "curtidas" in postagem else "",
            "comentarios": [{"comentario": p["comentario"], "comentario_id": str(p["comentario_id"]), "usuario_id": str(p["usuario_id"])} for p in postagem["comentarios"]] if "comentarios" in postagem else "",
            "usuario": self.usuario_helper(postagem["usuario"][0] if "usuario" in postagem else "")

        }