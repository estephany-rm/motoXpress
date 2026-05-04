from typing import List, Optional

from db.gestor_conexiones import connection_factory
from model.DAO.CategoriaDAO import CategoriaDAO
from model.VO.CategoriaVO import CategoriaVO


class CategoriaService:

    def listar_todas(self) -> List[CategoriaVO]:
        with connection_factory() as conn:
            return CategoriaDAO.listar_todas(conn)

    def obtener_por_id(self, id_categoria: int) -> Optional[CategoriaVO]:
        with connection_factory() as conn:
            return CategoriaDAO.obtener_por_id(conn, id_categoria)
