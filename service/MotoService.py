
from typing import List, Optional

from db.gestor_conexiones import connection_factory
from model.DAO.MotoDAO import MotoDAO
from model.DAO.MotoCategoriaDAO import MotoCategoriaDAO
from model.VO.MotoVO import MotoVO

_ESTADOS_VALIDOS = {'disponible', 'vendida', 'reservada'}


class MotoService:

    def listar_disponibles(self) -> List[MotoVO]:
        with connection_factory() as conn:
            return MotoDAO.listar_disponibles(conn)

    def obtener_detalle(self, id_moto: int) -> Optional[MotoVO]:
        # Carga eager: retorna la moto con sus categorías ya pobladas.
        with connection_factory() as conn:
            return MotoDAO.obtener_por_id(conn, id_moto)

    def registrar(self, moto: MotoVO,
                  ids_categorias: Optional[List[int]] = None) -> int:
        # Inserta una moto nueva y le asigna categorías opcionales.
        with connection_factory() as conn:
            if MotoDAO.buscar_por_vin(conn, moto.vin) is not None:
                raise ValueError(f"Ya existe una moto registrada con VIN '{moto.vin}'.")

            id_nuevo = MotoDAO.insertar(conn, moto)

            if ids_categorias:
                for id_cat in ids_categorias:
                    MotoCategoriaDAO.asignar(conn, id_nuevo, id_cat)

            return id_nuevo

    def cambiar_estado(self, id_moto: int, nuevo_estado: str) -> None:
        # Cambia el estado de una moto.
        if nuevo_estado not in _ESTADOS_VALIDOS:
            raise ValueError(
                f"Estado '{nuevo_estado}' no válido. "
                f"Valores permitidos: {_ESTADOS_VALIDOS}"
            )
        with connection_factory() as conn:
            moto = MotoDAO.obtener_por_id(conn, id_moto)
            if moto is None:
                raise ValueError(f"No existe ninguna moto con id {id_moto}.")
            MotoDAO.actualizar_estado(conn, id_moto, nuevo_estado)
