from typing import List, Optional

from db.gestor_conexiones import connection_factory
from model.DAO.EmpleadoDAO import EmpleadoDAO
from model.VO.EmpleadoVO import EmpleadoVO


class EmpleadoService:

    def listar(self) -> List[EmpleadoVO]:
        with connection_factory() as conn:
            return EmpleadoDAO.listar(conn)

    def listar_por_rol(self, rol: str) -> List[EmpleadoVO]:
        with connection_factory() as conn:
            return EmpleadoDAO.listar_por_rol(conn, rol)

    def obtener_por_id(self, id_empleado: int) -> Optional[EmpleadoVO]:
        with connection_factory() as conn:
            return EmpleadoDAO.obtener_por_id(conn, id_empleado)
